import requests

from mbta.errors import RateLimitError, InvalidQueryParameterError
from mbta import endpoints


class Client():
    """
    Class providing a client connection to the MBTA API.
    """
    def __init__(self, api_key: str):
        """
        Create a new Mbta Client object.

        Args:
            api_key: str
                Your MBTA api key.
        """
        self._session = requests.Session()
        self._session.headers = {
            'X-API-Key': api_key
        }

        self.rate_limit = {
            'x-ratelimit-limit': 20,
            'x-ratelimit-reset': 0,
            'x-ratelimit-remaining': 20,
        }

    def get_rate_limit(self):
        """The maximum number of requests you’re allowed to make per time window."""
        return self.rate_limit['x-ratelimit-limit']

    def get_rate_limit_remaining(self):
        """The number of requests remaining in the current time window."""
        return self.rate_limit['x-ratelimit-remaining']

    def get_rate_limit_reset(self):
        """The time at which the current rate limit time window ends in UTC epoch seconds."""
        return float(self.rate_limit['x-ratelimit-reset'])

    def get_lines(self,
                  page_offset: int = None,
                  page_limit: int = None,
                  sort: str = None,
                  fields_line: str = None,
                  include: str = None,
                  filter_id: str = None):
        """List of lines. A line is a combination of routes. This concept can be used to group similar routes when displaying them to customers, such as for routes which serve the same trunk corridor or bus terminal.

        Args:
            page_offset:
                Offset (0-based) of first element in the page
            page_limit:
                Max number of elements to return
            sort:
                Sort options:
                - color
                - long_name
                - short_name
                - sort_order
                - text_color
            fields_line:
                Fields to include with the response. Multiple fields MUST be a comma-separated (U+002C COMMA, “,”) list.
            include:
                Relationships to include
                - routes
            filter_id:
                Filter by multiple IDs. MUST be a comma-separated (U+002C COMMA, “,”) list.

        Return:
            requests.Response
                A list of lines.
        """
        url = endpoints.LINES
        params = {}

        if page_offset:
            params['page[offset]'] = page_offset

        if page_limit:
            params['page[limit]'] = page_limit

        if sort:
            if sort in ('color', '-color', 'long_name', '-long_name', 'short_name', '-short_name', 'sort_order', '-sort_order', 'text_color', '-text_color'):
                params['sort'] = sort
            else:
                raise InvalidQueryParameterError('Invalid query parameter value for sort: ' + sort)

        if fields_line:
            params['fields[line]'] = fields_line

        if include:
            if include == 'routes':
                params['include'] = include
            else:
                raise InvalidQueryParameterError('Invalid query parameter value for include: ' + include)

        if filter_id:
            params['filter[id]'] = filter_id

        resp = self._request(url, params)
        return resp

    def get_lines_id(self,
                     line_id: str,
                     fields_line: str = None,
                     include: str = None):
        """Single line, which represents a combination of routes.

        Args:
            line_id: (required)
                Unique ID for a line
            fields_line:
                Fields to include with the response. Multiple fields MUST be a comma-separated (U+002C COMMA, “,”) list.
            include:
                Relationships to include
                - routes
        Return:
            requests.Response
                A single line.
        """
        url = endpoints.LINES + line_id
        params = {}

        if line_id == '':
            raise InvalidQueryParameterError('line_id cannot be empty. If you do not need a specific line, use get_lines() instead')

        if fields_line:
            params['fields[line]'] = fields_line

        if include:
            if include == 'routes':
                params['include'] = include
            else:
                raise InvalidQueryParameterError('Invalid query parameter value for include: ' + include)

        resp = self._request(url, params)
        return resp

    def _request(self, url, params):
        """
        HTTP request to MBTA api.

        Args:
            url:
                The full url endpoint we want to retrieve data from.
            params:
                The query parameters being sent in the request.

        Return:
            requests.Response
        """
        # Check if rate limit exceeded before making request
        if self.rate_limit['x-ratelimit-remaining'] <= 0:
            raise RateLimitError('Rate limit exceeded.')

        # Make request
        resp = self._session.get(url, params=params)

        # Set rate limit status
        for key in self.rate_limit:
            self.rate_limit[key] = resp.headers.get(key)

        return resp

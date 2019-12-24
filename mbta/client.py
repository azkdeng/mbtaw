import requests


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
        self.session = requests.Session()
        self.session.headers = {
            'X-API-Key': api_key
        }

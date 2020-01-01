class MbtaError(Exception):
    """Base class for Mbta errors"""
    pass


class RateLimitError(MbtaError):
    """Exception raised when rate limited"""
    pass


class InvalidQueryParameterError(MbtaError):
    """Exception raised when providing an invalid query parameter"""
    pass

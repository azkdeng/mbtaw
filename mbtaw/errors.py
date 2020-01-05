class MbtawError(Exception):
    """Base class for Mbta errors"""
    pass


class RateLimitError(MbtawError):
    """Exception raised when rate limited"""
    pass


class InvalidQueryParameterError(MbtawError):
    """Exception raised when providing an invalid query parameter"""
    pass

from enum import StrEnum

class RESTType(StrEnum):
    """Simple enumerated type to track type of a REST request.
    """
    GET  = "GET"
    POST = "POST"
    PUT  = "PUT"

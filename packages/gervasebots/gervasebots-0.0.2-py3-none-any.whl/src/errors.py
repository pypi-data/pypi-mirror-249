class GervaseBotsError(Exception):
    """Base class for custom errors in GervaseBots."""

class APIClientError(GervaseBotsError):
    """Error raised for issues with the API client."""
    def __init__(self, message="API Client error"):
        self.message = message
        super().__init__(self.message)

class APITokenError(APIClientError):
    """Error raised for issues with API token."""
    def __init__(self, message="Invalid API Token"):
        self.message = message
        super().__init__(self.message)

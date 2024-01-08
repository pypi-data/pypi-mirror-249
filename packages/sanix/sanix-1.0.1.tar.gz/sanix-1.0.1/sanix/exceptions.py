"""Sanix exceptions."""

class SanixException(Exception):
    """Raised when Sanix API ended with error."""

    def __init__(self, status_code, status):
        """Initialize the Sanix Exception."""
        self.status_code = status_code
        self.status = status

"""Custom exceptions for municode library."""


class MunicodeError(Exception):
    """Base exception for municode library."""
    pass


class ScrapingError(MunicodeError):
    """Raised when scraping fails."""
    pass


class ParsingError(MunicodeError):
    """Raised when parsing fails."""
    pass


class InvalidUrlError(MunicodeError):
    """Raised when URL is invalid or malformed."""
    pass


class ElementNotFoundError(ScrapingError):
    """Raised when expected HTML element is not found."""
    pass

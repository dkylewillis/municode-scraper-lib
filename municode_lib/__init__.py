"""Municode scraper library for extracting municipal code data."""

from .scraper import MunicodeScraper
from .parser import MunicodeParser
from .models import Section, Document
from .exceptions import MunicodeError, ScrapingError, ParsingError

__version__ = "1.0.0"
__all__ = ["MunicodeScraper", "MunicodeParser", "Section", "Document", "MunicodeError", "ScrapingError", "ParsingError"]

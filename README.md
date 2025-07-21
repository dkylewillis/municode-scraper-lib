# Municode Scraper Library

A Python library for scraping and parsing municipal code documents from Municode websites.

## Features

- 🚀 Easy-to-use API for scraping municode content
- 📄 Parse HTML content into structured data
- 💾 Export to HTML and JSON formats
- 🔧 Configurable hierarchy parsing
- 🖥️ Command-line interface
- 🛡️ Error handling and validation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Scraping Municode Content

```python
from municode_lib import MunicodeScraper

# Simple scraping
with MunicodeScraper() as scraper:
    # Scrape a single section
    doc = scraper.scrape_section("https://library.municode.com/...")
    doc.save_html("output.html")
    doc.save_json("output.json")
```

### Parsing Existing HTML Files

```python
from municode_lib import MunicodeParser

parser = MunicodeParser()
doc = parser.parse_html_file("existing_file.html")
doc.save_json("parsed_output.json")
```

### Command Line Usage

```bash
# Scrape a single section
python -m municode_lib scrape "https://library.municode.com/..." --output data/

# Parse an HTML file
python -m municode_lib parse input.html --output parsed.json
```

## API Reference

### MunicodeScraper

Main class for scraping municode websites.

```python
scraper = MunicodeScraper(
    headless=True,          # Run browser in headless mode
    timeout=10,             # Page load timeout
    output_dir="data"       # Default output directory
)
```

### MunicodeParser

Parser for processing HTML content into structured data.

```python
parser = MunicodeParser(
    hierarchy_keywords=["Chapter", "Article", "Sec"],  # Hierarchy levels
    element_tags=["h2", "h3", "h4", "h5", "h6"]       # HTML tags for levels
)
```

## Project Structure

```
municode_lib/
├── __init__.py          # Package initialization
├── scraper.py           # Web scraping functionality
├── parser.py            # HTML parsing and processing
├── models.py            # Data models (Section, Document)
├── exceptions.py        # Custom exceptions
└── cli.py              # Command-line interface
```

## Requirements

- Python 3.7+
- selenium
- beautifulsoup4
- webdriver-manager
- htmlmin (optional, for HTML minification)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0
- Initial release
- Refactored from monolithic scripts into library structure
- Added structured data models
- Implemented CLI interface
- Added comprehensive error handling
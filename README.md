# Municode Library

A Python library for scraping and parsing municipal code data from Municode websites.

## Features

- **Web Scraping**: Extract municipal code content from Municode websites using Selenium
- **HTML Parsing**: Parse and structure HTML content into organized sections
- **Multiple Output Formats**: Save data as HTML or JSON
- **Easy-to-Use API**: Simple, intuitive interface for common tasks
- **Command-Line Interface**: CLI tools for quick operations
- **Error Handling**: Comprehensive error handling with custom exceptions

## Installation

### From Source

```bash
git clone <repository-url>
cd MunicodeScraper
pip install -r requirements_lib.txt
pip install -e .
```

### Dependencies

- Python 3.8+
- selenium
- beautifulsoup4
- webdriver-manager
- htmlmin
- lxml

## Quick Start

### Basic Usage

```python
from municode_lib import MunicodeScraper, MunicodeParser

# Scrape a single section
with MunicodeScraper() as scraper:
    document = scraper.scrape_section("https://library.municode.com/...")
    document.save_html("output.html")
    document.save_json("output.json")

# Parse existing HTML file
parser = MunicodeParser()
document = parser.parse_html_file("existing_file.html")
document.save_json("parsed_output.json")
```

### Command Line Usage

```bash
# Scrape a single section
python -m municode_lib.cli scrape "https://library.municode.com/..." --json

# Scrape full municode
python -m municode_lib.cli scrape "https://library.municode.com/..." --full --json

# Parse existing HTML file
python -m municode_lib.cli parse "input.html" -o "output.json"
```

## API Reference

### MunicodeScraper

Main class for web scraping operations.

```python
scraper = MunicodeScraper(
    headless=True,      # Run browser in headless mode
    timeout=10,         # Element wait timeout
    output_dir="data"   # Default output directory
)

# Scrape single section
document = scraper.scrape_section(url)

# Scrape full municode
documents = scraper.scrape_full(url)
```

### MunicodeParser

Class for parsing HTML content.

```python
parser = MunicodeParser(
    hierarchy_keywords=["Chapter", "Article", "Sec"],  # Hierarchy keywords
    element_tags=["h2", "h3", "h4", "h5", "h6"]       # HTML tags for levels
)

# Parse HTML file
document = parser.parse_html_file("file.html")

# Parse HTML string
document = parser.parse_html_string(html_content, title="Document Title")
```

### Document and Section Models

```python
# Document object
document.title          # Document title
document.sections       # List of Section objects
document.source_url     # Source URL
document.save_html()    # Save as HTML
document.save_json()    # Save as JSON

# Section object
section.title          # Section title
section.content        # HTML content
section.title_html     # Original title HTML
section.url           # Source URL
section.level         # Hierarchy level
section.path          # Hierarchy path
```

## Examples

### Example 1: Simple Scraping

```python
from municode_lib import MunicodeScraper

url = "https://library.municode.com/ga/coweta_county/codes/code_of_ordinances?nodeId=PTIICOOR_APXAZODE_ART6AHOOC"

with MunicodeScraper() as scraper:
    document = scraper.scrape_section(url)
    if document:
        print(f"Title: {document.title}")
        print(f"Sections: {len(document.sections)}")
        document.save_html("coweta_county.html")
```

### Example 2: Batch Processing

```python
from municode_lib import MunicodeScraper
from pathlib import Path

urls = [
    "https://library.municode.com/...",
    "https://library.municode.com/...",
]

output_dir = Path("scraped_data")
output_dir.mkdir(exist_ok=True)

with MunicodeScraper(output_dir=str(output_dir)) as scraper:
    for url in urls:
        try:
            document = scraper.scrape_section(url)
            if document:
                document.save_html(output_dir / f"{document.title}.html")
                document.save_json(output_dir / f"{document.title}.json")
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
```

### Example 3: Custom Parsing

```python
from municode_lib import MunicodeParser

# Custom hierarchy keywords for different municipality structure
parser = MunicodeParser(
    hierarchy_keywords=["Title", "Chapter", "Section", "Subsection"],
    element_tags=["h1", "h2", "h3", "h4"]
)

document = parser.parse_html_file("custom_format.html")
parser.save_structured_json(document, "structured_output.json")
```

## Error Handling

The library includes custom exceptions for better error handling:

```python
from municode_lib import MunicodeError, ScrapingError, ParsingError

try:
    with MunicodeScraper() as scraper:
        document = scraper.scrape_section(url)
except ScrapingError as e:
    print(f"Scraping failed: {e}")
except ParsingError as e:
    print(f"Parsing failed: {e}")
except MunicodeError as e:
    print(f"General municode error: {e}")
```

## Project Structure

```
MunicodeScraper/
├── municode_lib/           # Main library package
│   ├── __init__.py        # Package initialization
│   ├── scraper.py         # Web scraping functionality
│   ├── parser.py          # HTML parsing functionality
│   ├── models.py          # Data models
│   ├── exceptions.py      # Custom exceptions
│   └── cli.py            # Command-line interface
├── example_usage.py       # Usage examples
├── setup.py              # Package setup
├── requirements_lib.txt   # Library dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

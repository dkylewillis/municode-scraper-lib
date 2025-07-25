# Municode Scraper Library

A Python library for scraping and parsing municipal code documents from Municode websites.

## Features

- 🚀 Easy-to-use API for scraping municode content
- 📄 Parse HTML content into structured data
- 💾 Export to HTML and JSON formats
- 🔧 Configurable hierarchy parsing with path tracking
- 🖥️ Command-line interface
- 🛡️ Error handling and validation
- 🌳 Automatic hierarchy tree building and navigation paths

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

# Advanced scraping with hierarchy tracking
scraper = MunicodeScraper(
    hierarchy_keywords=["Chapter", "Article", "Sec"]  # Define hierarchy levels
)
doc = scraper.scrape_section("https://library.municode.com/...")

# Access hierarchy paths for each section
for section in doc.sections:
    print(f"Section: {section.label}")
    print(f"Path: {' > '.join(section.path)}")
    print(f"Title: {section.title}")
    print("---")
```

### Parsing Existing HTML Files

```python
from municode_lib import MunicodeParser

# Parse with hierarchy tracking
parser = MunicodeParser(hierarchy_keywords=["Chapter", "Article", "Sec"])
doc = parser.parse_html_file("existing_file.html")
doc.save_json("parsed_output.json")

# The parsed sections will include hierarchy paths
for section in doc.sections:
    print(f"{section.id}: {section.path}")  # Shows navigation path
```

### Command Line Usage

```bash
# Scrape a single section with hierarchy tracking
python -m municode_lib scrape "https://library.municode.com/..." --output data/

# Parse an HTML file with custom hierarchy levels
python -m municode_lib parse input.html --output parsed.json

# The output JSON will include hierarchy paths for navigation:
# {
#   "sections": [
#     {
#       "id": "chapter-22",
#       "path": ["chapter-22"],
#       "title": "CIVIL EMERGENCIES"
#     },
#     {
#       "id": "sec-22-1", 
#       "path": ["chapter-22", "article-i", "sec-22-1"],
#       "title": "Suspension of portions of Code..."
#     }
#   ]
# }
```

## API Reference

### MunicodeScraper

Main class for scraping municode websites.

```python
scraper = MunicodeScraper(
    headless=True,          # Run browser in headless mode
    timeout=10,             # Page load timeout
    output_dir="data",      # Default output directory
    hierarchy_keywords=["Chapter", "Article", "Sec"]  # Hierarchy levels for path tracking
)
```

**Hierarchy Path Tracking**: The scraper automatically builds navigation paths for each section based on the hierarchy keywords. Each section's `path` attribute contains the IDs of all parent sections plus its own ID, enabling easy navigation and breadcrumb generation.

### MunicodeParser

Parser for processing HTML content into structured data.

```python
parser = MunicodeParser(
    hierarchy_keywords=["Chapter", "Article", "Sec"],  # Hierarchy levels
    element_tags=["h2", "h3", "h4", "h5", "h6"]       # HTML tags for levels
)
```

**Hierarchy Path Tracking**: Like the scraper, the parser builds navigation paths by tracking section relationships. Each parsed section includes its full hierarchy path for easy navigation and organization.

## Data Structure

### Section Object

Each section contains the following attributes:

```python
{
    "id": "sec-22-3",                    # Unique identifier
    "title": "Prohibition of overcharging during state of emergency",
    "label": "Sec. 22-3.",              # Display label
    "content": "<div>...</div>",         # HTML content
    "path": [                            # Hierarchy navigation path
        "chapter-22",                    # Parent chapter
        "article-i",                     # Parent article  
        "sec-22-3"                       # Current section
    ],
    "url": "https://library.municode.com/..."
}
```

### Hierarchy Path Usage

The `path` attribute enables powerful navigation and organization:

```python
# Build breadcrumb navigation
breadcrumb = " > ".join(section.path)
print(f"You are here: {breadcrumb}")

# Find all sections in a specific chapter
chapter_sections = [s for s in doc.sections if s.path[0] == "chapter-22"]

# Find direct children of an article
article_children = [s for s in doc.sections 
                   if len(s.path) > 1 and s.path[1] == "article-i"]
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
- Added structured data models with hierarchy path tracking
- Implemented CLI interface
- Added comprehensive error handling
- **New**: Automatic hierarchy tree building and navigation paths
- **New**: Each section includes full parent-child relationship tracking
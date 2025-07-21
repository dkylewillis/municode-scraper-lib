"""Command-line interface for municode library."""

import argparse
import sys
from pathlib import Path

from .scraper import MunicodeScraper
from .parser import MunicodeParser
from .exceptions import MunicodeError


def scrape_command(args):
    """Handle scrape command."""
    try:
        with MunicodeScraper(headless=args.headless, output_dir=args.output) as scraper:
            if args.full:
                documents = scraper.scrape_full(args.url)
                print(f"✅ Scraped {len(documents)} documents")
                for doc in documents:
                    output_path = Path(args.output) / f"{doc.title}.html"
                    doc.save_html(output_path)
                    if args.json:
                        json_path = Path(args.output) / f"{doc.title}.json"
                        doc.save_json(json_path)
            else:
                document = scraper.scrape_section(args.url)
                if document:
                    print(f"✅ Scraped document: {document.title}")
                    output_path = Path(args.output) / f"{document.title}.html"
                    document.save_html(output_path)
                    if args.json:
                        json_path = Path(args.output) / f"{document.title}.json"
                        document.save_json(json_path)
                else:
                    print("❌ Failed to scrape document")
                    return 1
    except MunicodeError as e:
        print(f"❌ Scraping error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0


def parse_command(args):
    """Handle parse command."""
    try:
        parser = MunicodeParser()
        
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_path}")
            return 1
            
        document = parser.parse_html_file(str(input_path))
        print(f"✅ Parsed document: {document.title}")
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_suffix('.parsed.json')
            
        parser.save_structured_json(document, str(output_path))
        print(f"✅ Saved to: {output_path}")
        
    except MunicodeError as e:
        print(f"❌ Parsing error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Municode scraper and parser library",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape content from Municode website")
    scrape_parser.add_argument("url", help="Municode URL to scrape")
    scrape_parser.add_argument("-o", "--output", default="data", help="Output directory (default: data)")
    scrape_parser.add_argument("--full", action="store_true", help="Scrape full municode (vs single section)")
    scrape_parser.add_argument("--json", action="store_true", help="Also save as JSON")
    scrape_parser.add_argument("--headless", action="store_true", default=True, help="Run browser in headless mode")
    
    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Parse existing HTML file")
    parse_parser.add_argument("input", help="Input HTML file to parse")
    parse_parser.add_argument("-o", "--output", help="Output JSON file (default: input.parsed.json)")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "scrape":
        return scrape_command(args)
    elif args.command == "parse":
        return parse_command(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

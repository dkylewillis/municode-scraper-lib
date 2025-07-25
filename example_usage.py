"""
Example usage of the refactored municode library.
"""

from pathlib import Path
from municode_lib import MunicodeScraper, MunicodeParser, MunicodeError


def main():
    """Demonstrate library usage."""
    
    # Example URLs
    url1 = "https://library.municode.com/ga/coweta_county/codes/code_of_ordinances?nodeId=PTIICOOR_APXAZODE"
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    try:
        # Example 1: Scrape a single section with custom hierarchy
        print("=== Scraping Single Section ===")
        
        # Define hierarchy for this specific municode
        hierarchy_keywords = ["Appendix", "Chapter", "Article", "Sec"]
        
        with MunicodeScraper(
            headless=True, 
            output_dir="data",
            hierarchy_keywords=hierarchy_keywords
        ) as scraper:
            document = scraper.scrape_section(url1)
            if document:
                print(f"Scraped document: {document.title}")
                print(f"Number of sections: {len(document.sections)}")
                
                # Print section hierarchy for debugging
                print("\n=== Section Hierarchy ===")
                for section in document.sections:
                    indent = "  " * len(section.path)
                    print(f"{indent}{section.label}: {section.title}")
                    print(f"{indent}  Path: {section.path}")
                    print(f"{indent}  ID: {section.id}")
                    print()
                
                # Save in different formats
                document.save_html(data_dir / f"{document.title}.html")
                document.save_json(data_dir / f"{document.title}.json")
                print(f"Saved document as HTML and JSON")
        
        # Example 2: Parse existing HTML file (if available)
        # print("\n=== Parsing Existing HTML ===")
        # html_files = list(data_dir.glob("*.html"))
        # if html_files:
        #     parser = MunicodeParser()
        #     for html_file in html_files[:1]:  # Parse first file only
        #         try:
        #             document = parser.parse_html_file(str(html_file))
        #             print(f"Parsed document: {document.title}")
        #             print(f"Number of sections: {len(document.sections)}")
                    
        #             # Save processed version
        #             # parser.save_structured_json(
        #             #     document, 
        #             #     data_dir / f"{document.title}_structured.json"
        #             # )
        #         except Exception as e:
        #             print(f"Failed to parse {html_file}: {e}")
        
        # Example 3: Scrape full municode (commented out as it takes longer)
        # print("\n=== Scraping Full Municode ===")
        # with MunicodeScraper() as scraper:
        #     documents = scraper.scrape_full(url2)
        #     print(f"Scraped {len(documents)} documents")
        #     for doc in documents:
        #         doc.save_html(data_dir / f"{doc.title}.html")
        
    except MunicodeError as e:
        print(f"Municode error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

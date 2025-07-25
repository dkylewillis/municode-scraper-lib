"""Parser for municode HTML content."""

import re
import json
from typing import List, Optional
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

# Optional import for htmlmin
try:
    import htmlmin
    HAS_HTMLMIN = True
except ImportError:
    HAS_HTMLMIN = False

from .models import Section, Document, parse_section_title
from .exceptions import ParsingError


class MunicodeParser:
    """Parser for processing municode HTML content."""
    
    def __init__(self, hierarchy_keywords: Optional[List[str]] = None, element_tags: Optional[List[str]] = None):
        """
        Initialize the parser.
        
        Args:
            hierarchy_keywords: Keywords for hierarchy levels (default: ["Chapter", "Article", "Sec"])
            element_tags: HTML tags for each hierarchy level (default: ["h2", "h3", "h4", "h5", "h6"])
        """
        self.hierarchy_keywords = hierarchy_keywords or ["Chapter", "Article", "Sec"]
        self.element_tags = element_tags or ["h2", "h3", "h4", "h5", "h6"]
    
    def _get_level(self, tag, prefix: str) -> Optional[int]:
        """Extract increment or content level from CSS class."""
        if not hasattr(tag, "get"):
            return None
        for cls in tag.get("class", []):
            m = re.match(rf"{prefix}(\d+)", cls)
            if m:
                return int(m.group(1))
        return None

    def _indent_html(self, level: int) -> str:
        """Generate HTML indentation using non-breaking spaces."""
        return '&nbsp;' * (4 * level)

    def _remove_first_heading(self, html_content: str) -> str:
        """Remove the first heading tag from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        first_heading = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"])
        if first_heading:
            first_heading.decompose()
        return str(soup)

    def _process_chunk(self, chunk, soup, current_path: List[Optional[str]]) -> dict:
        """Process a single content chunk and return section data."""
        children = list(chunk.children)
        result = []
        prev = chunk.previous_sibling
        title = "Untitled Section"
        
        # Handle whitespace in previous siblings
        while prev and isinstance(prev, NavigableString) and not prev.strip():
            prev = prev.previous_sibling
        
        # Check for hierarchy keywords in previous sibling
        for i, keyword in enumerate(self.hierarchy_keywords):
            if prev and isinstance(prev, NavigableString) and keyword.lower() in prev.lower():
                title = prev.strip()
                
                # Update hierarchy path
                current_path[i] = title
                for j in range(i + 1, len(current_path)):
                    current_path[j] = None  # Clear lower levels
                
                # Create new heading element
                tag = self.element_tags[i] if i < len(self.element_tags) else "h2"
                new_el = soup.new_tag(tag, **{"class": "chunk-title"})
                new_el.string = title
                result.append(new_el)
                prev.extract()  # Remove the previous sibling
                break

            # if isinstance(prev, Tag) and keyword.lower() in prev.text.lower():
            #     title = prev.text.strip()
                
            #     # Update hierarchy path
            #     current_path[i] = title
            #     for j in range(i + 1, len(current_path)):
            #         current_path[j] = None  # Clear lower levels
            #     break

        # Process child elements
        i = 0
        while i < len(children):
            el = children[i]

            if el.name == "p" and (lvl := self._get_level(el, "incr")) is not None:
                label = el.get_text(strip=True)
                content_el = el.find_next_sibling()
                content = content_el.decode_contents().strip() if content_el else ""

                # Combine into one paragraph with indentation
                indent = self._indent_html(lvl)
                combined = f"{indent}{label} {content}".strip()
                p = soup.new_tag("p")
                p.append(BeautifulSoup(combined, "html.parser"))
                result.append(p)

            elif el.name == "p" and self._get_level(el, "content") is not None:
                # Skip orphaned contentX elements
                pass
            else:
                result.append(el)

            i += 1

        # Replace old content with processed content
        chunk.clear()
        for tag in result:
            chunk.append(tag)

        # Minify the HTML content
        if HAS_HTMLMIN:
            minified_content = htmlmin.minify(
                chunk.decode_contents(), 
                remove_comments=True, 
                remove_empty_space=True
            )
        else:
            # Fallback: just get the content without minification
            minified_content = chunk.decode_contents()

        return {
            "path": [p for p in current_path if p],
            "title": title,
            "content": self._remove_first_heading(minified_content)
        }

    def parse_html_file(self, filepath: str, title: Optional[str] = None) -> Document:
        """
        Parse HTML file and return structured Document.
        
        Args:
            filepath: Path to the HTML file
            title: Optional title for the document (defaults to filename)
            
        Returns:
            Document object containing parsed sections
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise ParsingError(f"File not found: {filepath}")
        
        if title is None:
            title = filepath.stem
            
        try:
            with open(filepath, encoding="utf-8") as f:
                return self.parse_html_string(f.read(), title, str(filepath))
        except Exception as e:
            raise ParsingError(f"Failed to parse file {filepath}: {e}")

    def parse_html_string(self, html_content: str, title: str = "Untitled", source_url: str = "") -> Document:
        """
        Parse HTML string and return structured Document.
        
        Args:
            html_content: HTML content to parse
            title: Title for the document
            source_url: Source URL or file path
            
        Returns:
            Document object containing parsed sections
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            current_path = [None] * len(self.hierarchy_keywords)
            sections = []
            
            # Process each content chunk
            for chunk in soup.find_all("div", class_="chunk-content"):
                chunk_data = self._process_chunk(chunk, soup, current_path)
                
                # Parse the title to extract id, label, and title components
                section_id, label, parsed_title = parse_section_title(chunk_data["title"])
                
                # Include current section ID in path
                section_path = chunk_data["path"].copy()
                section_path.append(section_id)
                
                section = Section(
                    id=section_id,
                    title=parsed_title,
                    label=label,
                    content=chunk_data["content"],
                    path=section_path,
                    url=source_url
                )
                sections.append(section)
            
            return Document(title=title, sections=sections, source_url=source_url)
            
        except Exception as e:
            raise ParsingError(f"Failed to parse HTML content: {e}")

    def save_processed_html(self, document: Document, output_path: str) -> None:
        """
        Save processed document as HTML file.
        
        Args:
            document: Document to save
            output_path: Path for output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"<h1>{document.title}</h1>\n")
                for section in document.sections:
                    f.write(section.content)
                    f.write("\n")
            print(f"Saved processed HTML to {output_path}")
        except Exception as e:
            raise ParsingError(f"Failed to save HTML file: {e}")

    def save_structured_json(self, document: Document, output_path: str) -> None:
        """
        Save document as structured JSON file.
        
        Args:
            document: Document to save
            output_path: Path for output JSON file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(document.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"Saved structured JSON to {output_path}")
        except Exception as e:
            raise ParsingError(f"Failed to save JSON file: {e}")

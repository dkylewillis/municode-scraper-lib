"""Data models for municode content."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import json
import re


def parse_section_title(full_title: str) -> Tuple[str, str, str]:
    """
    Parse a full section title into id, label, and title components.
    
    Args:
        full_title: Full title like "Article II - Some Title" or "Sec. 22-1. - Emergency procedures"
        
    Returns:
        Tuple of (id, label, title)
    """
    # Split on the first dash to separate label from title
    if " - " in full_title:
        label_part, title_part = full_title.split(" - ", 1)
        
        # Clean up the parts
        label = label_part.strip()
        title = title_part.strip()
        
        # Create ID by normalizing the label part
        # Remove periods, convert to lowercase, replace spaces with hyphens
        section_id = re.sub(r'[.\s]+', '-', label).lower().strip('-')
        
        return section_id, label, title
    else:
        # Fallback: no dash separator found
        clean_title = full_title.strip()
        # Create a simple ID from the beginning of the title
        fallback_id = re.sub(r'[^\w\s]', '', clean_title[:20]).lower().replace(' ', '-').strip('-')
        return fallback_id, clean_title, clean_title


@dataclass
class Section:
    """Represents a single municode section."""
    id: str
    title: str
    label: str
    content: str
    path: List[str] = field(default_factory=list)
    url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert section to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'label': self.label,
            'content': self.content,
            'path': self.path,
            'url': self.url
        }


@dataclass
class Document:
    """Represents a complete municode document."""
    title: str
    sections: List[Section]
    source_url: str
    
    def save_html(self, filepath: Path) -> None:
        """Save document as HTML file."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"<h1>{self.title}</h1>\n")
            for section in self.sections:
                f.write(f"<h2>{section.title}</h2>\n")
                f.write(section.content)
                f.write("\n")
    
    def save_json(self, filepath: Path) -> None:
        """Save document as JSON file."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'title': self.title,
            'source_url': self.source_url,
            'sections': [section.to_dict() for section in self.sections]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            'title': self.title,
            'source_url': self.source_url,
            'sections': [section.to_dict() for section in self.sections]
        }

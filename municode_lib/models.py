"""Data models for municode content."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import json


@dataclass
class Section:
    """Represents a single municode section."""
    title: str
    content: str
    title_html: str = ""
    url: Optional[str] = None
    level: int = 0
    path: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert section to dictionary."""
        return {
            'title': self.title,
            'content': self.content,
            'title_html': self.title_html,
            'url': self.url,
            'level': self.level,
            'path': self.path
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

#!/usr/bin/env python3
"""Quick test for hierarchy path tracking."""

from municode_lib.scraper import MunicodeScraper

def test_hierarchy_tree():
    """Test the hierarchy tree logic."""
    scraper = MunicodeScraper(hierarchy_keywords=["Chapter", "Article", "Sec"])
    
    # Simulate the hierarchy state
    current_hierarchy = [None, None, None]
    
    # Test Chapter level
    path1 = scraper._update_hierarchy_tree(current_hierarchy, 0, "chapter-22")
    print(f"Chapter 22 path: {path1}")
    print(f"Hierarchy state: {current_hierarchy}")
    
    # Test Article level
    path2 = scraper._update_hierarchy_tree(current_hierarchy, 1, "article-i")
    print(f"Article I path: {path2}")
    print(f"Hierarchy state: {current_hierarchy}")
    
    # Test Section level
    path3 = scraper._update_hierarchy_tree(current_hierarchy, 2, "sec-22-1")
    print(f"Sec. 22-1 path: {path3}")
    print(f"Hierarchy state: {current_hierarchy}")
    
    # Test another Section at same level
    path4 = scraper._update_hierarchy_tree(current_hierarchy, 2, "sec-22-2")
    print(f"Sec. 22-2 path: {path4}")
    print(f"Hierarchy state: {current_hierarchy}")

if __name__ == "__main__":
    test_hierarchy_tree()

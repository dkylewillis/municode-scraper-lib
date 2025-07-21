from bs4 import BeautifulSoup, NavigableString
import re
from pathlib import Path
import json
import htmlmin
import html

# Could updata to make this more dynamic
# May need a list for each level, as some levels may contain multiple keywords like Sec and Section, or Article and Appendix

hierarchy_keywords = ["Chapter", "Article", "Sec"]
element_tags = ["h2", "h3", "h4", "h5", "h6"]

# Load your input HTML
with open("data/APPENDIX A - ZONING AND DEVELOPMENT.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

open_file = Path(f.name).stem
# Helper: Extract incr or content level from class

def get_level(tag, prefix):
    if not hasattr(tag, "get"):
        return None
    for cls in tag.get("class", []):
        m = re.match(rf"{prefix}(\d+)", cls)
        if m:
            return int(m.group(1))
    return None

# Helper: generate &nbsp; indentation
def indent_html(level):
    return '&nbsp;' * (4 * level)

def remove_first_heading(html):
    soup = BeautifulSoup(html, "html.parser")
    # Find the first heading tag (h1 to h6)
    first_heading = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"])
    if first_heading:
        first_heading.decompose()  # Removes the tag from the soup
    return str(soup)

# Process each content chunk
current_path = [None] * len(hierarchy_keywords)
json_data = []
for chunk in soup.find_all("div", class_="chunk-content"):
    children = list(chunk.children)
    i = 0
    result = []
    prev = chunk.previous_sibling
    ## Supposedly is better at handling whitespace
    while prev and isinstance(prev, NavigableString) and not prev.strip():
        prev = prev.previous_sibling
    
    for i, keyword in enumerate(hierarchy_keywords):
        if prev and isinstance(prev, NavigableString) and keyword.lower() in prev.lower():
            # If the previous sibling is a string containing a hierarchy keyword
            # we assume it is the title of the chunk
            title = prev.strip()

            # Update hierarchy path
            current_path[i] = title
            for j in range(i + 1, len(current_path)):
                current_path[j] = None  # Clear lower levels
            
            # (Optional) print or store full path
            full_path = [p for p in current_path if p]
            tag = element_tags[i] if i < len(element_tags) else "h2"
            new_el = soup.new_tag(tag, **{"class": "chunk-title"})
            new_el.string = title
            result.append(new_el)
            prev.extract()  # Remove the previous sibling

    while i < len(children):
        el = children[i]

        if el.name == "p" and (lvl := get_level(el, "incr")) is not None:
            label = el.get_text(strip=True)
            content = el.find_next_sibling()
            content = content.decode_contents().strip()

            # Combine into one <p>
            indent = indent_html(lvl)
            combined = f"{indent}{label} {content}".strip()
            p = soup.new_tag("p")
            p.append(BeautifulSoup(combined, "html.parser"))
            result.append(p)

        elif el.name == "p" and get_level(el, "content") is not None:
            # Skip orphaned contentX
            pass
        else:
            result.append(el)

        i += 1

    # Replace old content
    chunk.clear()
    for tag in result:
        chunk.append(tag)

    chunk = minified_html = htmlmin.minify(chunk.decode_contents(), remove_comments=True, remove_empty_space=True)

    json_data.append({
        "path": [p for p in current_path if p],
        "title": title,
        "text": remove_first_heading(chunk)
    })
    
# Save the modified HTML

output_path = f"data/{open_file}.mod.html"
with open(output_path, "w", encoding="utf-8") as f:
    filename = f.name.split("/")[-1]
    soup = htmlmin.minify(str(soup), remove_comments=True, remove_empty_space=True)
    f.write(f"<h1>{open_file}</h1>\n")
    f.write(str(soup))

print(f"Saved output to {output_path}")

# Write JSON
json_output_path = f"data/{open_file}.json"
with open(json_output_path, "w", encoding="utf-8") as jf:
    json.dump(json_data, jf, indent=2, ensure_ascii=False)
print(f"Saved JSON to {json_output_path}")
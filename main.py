from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class ParsedDocument:
    text: List[str] = field(default_factory=list)
    images: List[Dict[str, Any]] = field(default_factory=list)

def parse_multimodal(doc: Dict[str, Any]) -> ParsedDocument:
    result = ParsedDocument()
    for block in doc.get("blocks", []):
        kind = block.get("type")
        if kind == "text":
            content = block.get("content", "").strip()
            if content:
                result.text.append(content)
        elif kind == "image":
            result.images.append({
                "id": block.get("id"),
                "alt": block.get("alt", ""),
                "width": block.get("width"),
                "height": block.get("height"),
            })
    return result

def summarize(parsed: ParsedDocument) -> str:
    text_len = sum(len(t) for t in parsed.text)
    return f"Parsed {len(parsed.text)} text block(s) ({text_len} chars) and {len(parsed.images)} image(s)."

def main():
    payload = {
        "blocks": [
            {"type": "text", "content": "Welcome to multi-modal parsing."},
            {"type": "image", "id": "img-1", "alt": "chart", "width": 640, "height": 480},
            {"type": "text", "content": "Extract text and image metadata."},
            {"type": "image", "id": "img-2", "alt": "diagram", "width": 800, "height": 600},
        ]
    }
    parsed = parse_multimodal(payload)
    print("Text blocks:")
    for idx, text in enumerate(parsed.text, 1):
        print(f"  {idx}. {text}")
    print("Images:")
    for image in parsed.images:
        print(f"  - {image['id']}: alt={image['alt']!r}, size={image['width']}x{image['height']}")
    print(summarize(parsed))

if __name__ == "__main__":
    main()

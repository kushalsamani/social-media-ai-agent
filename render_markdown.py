import json
from pathlib import Path

# JSON input files (relative to project root)
JSON_FILES = [
    ("resources/drafts/post_drafts.json", "post_drafts"),
    ("resources/drafts/reel_scripts.json", "reel_scripts"),
    ("resources/drafts/blogs/blog_drafts.json", "blogs"),
    ("resources/drafts/seo_optimized_content.json", "seo")
]

BASE_OUTPUT_FOLDER = Path("resources/rendered")

# Utility to clean titles for a filename
def sanitize_filename(text: str) -> str:
    return "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in text).replace(" ", "_")


def render_markdown(item: dict) -> str:
    tags = ", ".join(item.get("tags", []))
    md = f"""# {item['topic']}

**Content Type:** {item['content_type']}  
**Target Audience:** {item['target_audience']}  
**Tags:** {tags}

---

{item['content'].strip()}

"""
    return md


def process_file(json_path: str, subfolder: str):
    path = Path(json_path)

    if not path.exists():
        print(f"⚠️  File not found: {path}")
        return

    print(f"➡️  Processing JSON → {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create a subfolder under rendered/
    out_folder = BASE_OUTPUT_FOLDER / subfolder
    out_folder.mkdir(parents=True, exist_ok=True)

    for item in data.get("items", []):
        filename = sanitize_filename(f"{item['content_type']}_{item['topic']}.md")
        output_path = out_folder / filename

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(render_markdown(item))

        print(f"   📝 Saved: {output_path}")


if __name__ == "__main__":
    for jfile, sub in JSON_FILES:
        process_file(jfile, sub)

    print("\n✅ Rendering complete!")

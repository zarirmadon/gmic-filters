import os
import re

ROOT_DIR = "."
README_PATH = "README.md"
IGNORE_DIRS = {".git", ".github", "scripts", "assets", "docs", "node_modules", ".vscode"}

# List of common preview image file names to search for
IMAGE_NAMES = [
    "preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.gif",
    "thumb.png", "thumb.jpg", "thumb.jpeg", "thumb.webp",
    "cover.png", "cover.jpg", "cover.jpeg"
]


def find_preview_image(folder_path):
    """
    Searches for a preview image in either:
    1. The plugin root directory (e.g., ./Film-Emulation/preview.png)
    2. An 'images', 'assets', or 'docs' subfolder (e.g., ./Film-Emulation/images/preview.png)
    """
    search_locations = [
        folder_path,
        os.path.join(folder_path, "images"),
        os.path.join(folder_path, "assets"),
        os.path.join(folder_path, "docs")
    ]

    for location in search_locations:
        if os.path.exists(location) and os.path.isdir(location):
            # Check for explicitly named preview files
            for img_name in IMAGE_NAMES:
                candidate = os.path.join(location, img_name)
                if os.path.isfile(candidate):
                    # Ensure POSIX paths for URL/GitHub rendering compatibility
                    return candidate.replace("\\", "/")
            
            # Fallback: pick the first supported image file found in the location
            for file in os.listdir(location):
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                    return os.path.join(location, file).replace("\\", "/")

    return None


def extract_description(folder_path):
    """
    Extracts the first paragraph or description from the plugin folder's sub-README.md.
    """
    sub_readme = os.path.join(folder_path, "README.md")
    if os.path.exists(sub_readme):
        with open(sub_readme, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                # Skip headers, empty lines, and raw HTML tags
                if line and not line.startswith("#") and not line.startswith("<"):
                    # Strip markdown links e.g. [text](link) -> text
                    clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)
                    # Limit length to 120 characters with ellipsis
                    return clean[:120] + "..." if len(clean) > 120 else clean
                    
    return "Custom G'MIC filter plugin."


def build_html_table():
    """
    Scans top-level plugin folders and constructs a GitHub-friendly HTML table.
    """
    folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(f) and f not in IGNORE_DIRS]
    folders.sort()

    html = "<table>\n  <thead>\n    <tr>\n"
    html += '      <th align="center" width="22%">Preview</th>\n'
    html += '      <th align="left" width="25%">Plugin / Folder</th>\n'
    html += '      <th align="left" width="41%">Description</th>\n'
    html += '      <th align="center" width="12%">Explore</th>\n'
    html += "    </tr>\n  </thead>\n  <tbody>\n"

    for folder in folders:
        desc = extract_description(folder)
        img_path = find_preview_image(folder)

        # Build preview HTML thumbnail column
        if img_path:
            img_html = f'<a href="./{folder}"><img src="./{img_path}" alt="{folder} Preview" width="140" style="border-radius: 6px;" min-height="70" /></a>'
        else:
            # Fallback placeholder if no image exists in plugin folder or subfolders
            img_html = f'<a href="./{folder}"><code>[ No Preview ]</code></a>'

        html += "    <tr>\n"
        html += f'      <td align="center">{img_html}</td>\n'
        html += f"      <td><b>📂 {folder}</b></td>\n"
        html += f"      <td>{desc}</td>\n"
        html += f'      <td align="center"><a href="./{folder}"><code>View ➔</code></a></td>\n'
        html += "    </tr>\n"

    html += "  </tbody>\n</table>"
    return html


def update_main_readme():
    """
    Injects the generated HTML table into README.md between the target markers.
    """
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_table = build_html_table()
    pattern = r"<!-- START_PLUGIN_SECTION -->.*?<!-- END_PLUGIN_SECTION -->"
    replacement = f"<!-- START_PLUGIN_SECTION -->\n{new_table}\n<!-- END_PLUGIN_SECTION -->"

    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated README.md plugin directory!")
    else:
        print("Warning: Could not find <!-- START_PLUGIN_SECTION --> markers in README.md.")


if __name__ == "__main__":
    update_main_readme()
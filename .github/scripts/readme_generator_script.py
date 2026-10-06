import os
import re

ROOT_DIR = "."
README_PATH = "README.md"
IGNORE_DIRS = {".git", ".github", "scripts", "assets", "docs", "node_modules", ".vscode"}

IMAGE_NAMES = [
    "preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.gif",
    "thumb.png", "thumb.jpg", "thumb.jpeg", "thumb.webp",
    "cover.png", "cover.jpg", "cover.jpeg"
]


def find_preview_image(folder_path):
    """
    Searches for a preview image in the folder root or subdirectories (images, assets, docs).
    """
    search_locations = [
        folder_path,
        os.path.join(folder_path, "images"),
        os.path.join(folder_path, "assets"),
        os.path.join(folder_path, "docs")
    ]

    for location in search_locations:
        if os.path.exists(location) and os.path.isdir(location):
            for img_name in IMAGE_NAMES:
                candidate = os.path.join(location, img_name)
                if os.path.isfile(candidate):
                    return candidate.replace("\\", "/")

            for file in os.listdir(location):
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                    return os.path.join(location, file).replace("\\", "/")

    return None


def extract_metadata(folder_path):
    """
    Extracts title (from first `# Title` line) and description (first text line after title)
    from the plugin's sub-README.md.
    """
    sub_readme = os.path.join(folder_path, "README.md")
    title = folder_path.replace("-", " ").replace("_", " ").title()
    description = "Custom G'MIC filter plugin script."

    if os.path.exists(sub_readme):
        with open(sub_readme, "r", encoding="utf-8") as f:
            lines = f.readlines()

        extracted_title = None
        extracted_desc = None

        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            # Check for title (# Header)
            if not extracted_title and clean_line.startswith("#"):
                extracted_title = re.sub(r"^#+\s*", "", clean_line).strip()
                continue

            # Check for description line (skip images, html, badges)
            if extracted_title and not extracted_desc and not clean_line.startswith(("#", "<", "!", "[")):
                clean_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
                clean_text = re.sub(r'[*_`]', '', clean_text)
                extracted_desc = clean_text[:140] + "..." if len(clean_text) > 140 else clean_text
                break

        if extracted_title:
            title = extracted_title
        if extracted_desc:
            description = extracted_desc

    return title, description


def build_plugin_list_html():
    """
    Constructs a clean, borderless list layout with horizontal rule separators.
    """
    folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(f) and f not in IGNORE_DIRS]
    folders.sort()

    html = '<table width="100%" border="0" cellspacing="0" cellpadding="12">\n  <tbody>\n'

    for index, folder in enumerate(folders):
        title, desc = extract_metadata(folder)
        img_path = find_preview_image(folder)

        if img_path:
            img_html = f'<a href="./{folder}"><img src="./{img_path}" alt="{folder} Preview" width="150" style="border-radius: 8px;" /></a>'
        else:
            img_html = f'<a href="./{folder}"><code>[ No Preview ]</code></a>'

        html += '    <tr>\n'
        html += f'      <td align="center" width="22%" valign="middle">\n        {img_html}\n      </td>\n'
        html += f'      <td align="left" valign="middle">\n'
        html += f'        <h3><a href="./{folder}">📂 {title}</a></h3>\n'
        html += f'        <p>{desc}</p>\n'
        html += f'        <a href="./{folder}"><code>Explore Filter ➔</code></a>\n'
        html += f'      </td>\n'
        html += '    </tr>\n'

        # Add divider separator line between entries
        if index < len(folders) - 1:
            html += '    <tr><td colspan="2"><hr style="border: 0; border-top: 1px solid #30363d;" /></td></tr>\n'

    html += '  </tbody>\n</table>'
    return html


def update_main_readme():
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_section = build_plugin_list_html()
    pattern = r"<!-- START_PLUGIN_SECTION -->.*?<!-- END_PLUGIN_SECTION -->"
    replacement = f"<!-- START_PLUGIN_SECTION -->\n{new_section}\n<!-- END_PLUGIN_SECTION -->"

    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated README.md plugin directory!")
    else:
        print("Warning: Could not find <!-- START_PLUGIN_SECTION --> markers in README.md.")


if __name__ == "__main__":
    update_main_readme()
```

### Key Improvements Made:
1. **Gridless Clean Separators**: Replaced table grid lines with clean horizontal line dividers (`<hr/>`) between filters for a modern feed look.
2. **Sub-README Title & Description Extraction**:
   - The Python script now parses each folder's `README.md` for the main heading (`# Title`) and uses it as the entry title.
   - It captures the first meaningful text line following the heading for the description.
3. **Card Accents**: Added colored callout containers (`<blockquote>`) around the main repository taglines and installation commands.

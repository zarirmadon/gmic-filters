from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

START = "<!-- FILTER_INDEX_START -->"
END = "<!-- FILTER_INDEX_END -->"

IGNORE = {".git", ".github"}

entries = []

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir() or folder.name in IGNORE:
        continue

    readme = folder / "README.md"
    if not readme.exists():
        continue

    text = readme.read_text(encoding="utf-8")

    title_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not title_match:
        continue

    title = title_match.group(1).strip()
    remainder = text[title_match.end():]
    description = ""

    for block in re.split(r"\n\s*\n", remainder):
        block = block.strip()

        if not block or block.startswith("<br") or block.startswith("<!--"):
            continue

        if block.startswith(">"):
            block = re.sub(r"^>\s?", "", block, flags=re.MULTILINE)

        if block.startswith("#"):
            continue

        block = block.replace("**", "").strip()
        description = " ".join(block.split())
        break

    if not description:
        continue

    entries.append(
        f"### [{title}](./{folder.name}/)\n\n"
        f"{description}\n\n"
        f"<br>"
    )

index = "\n\n".join(entries)

root_text = README.read_text(encoding="utf-8")

if START not in root_text or END not in root_text:
    raise SystemExit(
        "Root README.md is missing FILTER_INDEX_START / FILTER_INDEX_END markers."
    )

before, rest = root_text.split(START, 1)
_, after = rest.split(END, 1)

new_text = (
    before
    + START
    + "\n\n"
    + index
    + "\n\n"
    + END
    + after
)

README.write_text(new_text, encoding="utf-8")

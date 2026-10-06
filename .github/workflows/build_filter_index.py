#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START = "<!-- FILTER_INDEX_START -->"
END = "<!-- FILTER_INDEX_END -->"
IGNORE = {".git", ".github"}

def clean_inline(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("**","").replace("__","").replace("`","")
    return " ".join(text.split()).strip()

def description_from_readme(text, heading_end):
    # Proven conservative approach: only accept a clean prose paragraph.
    body = re.sub(r"<!--.*?-->", "", text[heading_end:], flags=re.S)
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b:
            continue
        if b.startswith(("#", "![", "[![", "```", "<")):
            continue
        if "user-attachments/" in b or "img.shields.io/" in b:
            continue
        # Skip blocks dominated by links/badges/metadata.
        if b.count("](") > 1:
            continue
        if b.startswith(">"):
            b = re.sub(r"^>\s?", "", b, flags=re.M)
        b = clean_inline(b)
        if 30 <= len(b) <= 500:
            return b
    return "Documentation, source and usage information for this G'MIC filter."

def discover():
    items=[]
    for folder in sorted(ROOT.iterdir(), key=lambda p:p.name.casefold()):
        if not folder.is_dir() or folder.name in IGNORE:
            continue
        child = folder/"README.md"
        if not child.is_file():
            continue
        text=child.read_text(encoding="utf-8", errors="replace")
        h=re.search(r"^#\s+(.+?)\s*$", text, flags=re.M)
        if h:
            title=clean_inline(h.group(1))
            title=re.sub(r"^[^\w'“\"]+\s*", "", title)
            desc=description_from_readme(text,h.end())
        else:
            title=folder.name.replace("-"," ").title()
            desc=description_from_readme(text,0)
        items.append((folder.name,title,desc))
    return items

def render(folder,title,desc):
    # GitHub README HTML is intentionally conservative: no unsupported CSS,
    # no fake cards. The linked heading is the sole navigation target.
    return (
        f'<h3><a href="./{folder}/">{title}</a></h3>\n\n'
        f'<p>{desc}</p>'
    )

def main():
    source=README.read_text(encoding="utf-8")
    if START not in source or END not in source:
        raise SystemExit("README.md is missing filter-index markers.")
    before,rest=source.split(START,1)
    _,after=rest.split(END,1)
    index="\n\n<br>\n\n".join(render(*item) for item in discover())
    result=before+START+"\n\n"+index+"\n\n"+END+after
    if result != source:
        README.write_text(result,encoding="utf-8")

if __name__=="__main__":
    main()

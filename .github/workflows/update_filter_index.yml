#!/usr/bin/env python3
from pathlib import Path
import html, re

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START = "<!-- FILTER_INDEX_START -->"
END = "<!-- FILTER_INDEX_END -->"
IGNORE_DIRS = {".git", ".github", ".breeze-icons"}

def strip_md(v):
    v=re.sub(r"<!--.*?-->","",v,flags=re.S)
    v=re.sub(r"!\\[[^\\]]*\\]\\([^)]*\\)","",v)
    v=re.sub(r"\\[(.*?)\\]\\([^)]*\\)",r"\\1",v)
    v=re.sub(r"<[^>]+>","",v)
    v=v.replace("**","").replace("__","").replace("`","")
    return " ".join(v.split()).strip()

def clean_title(v):
    return re.sub(r"^[^\\w'“\"]+\\s*","",strip_md(v)).strip()

def first_description(text, start):
    """Return the first clean prose paragraph, never README metadata."""
    text = re.sub(r"<!--.*?-->", "", text[start:], flags=re.S)
    lines = text.splitlines()
    paragraph = []

    def usable(line):
        x = line.strip()
        if not x:
            return None
        if x.startswith(("#", "![", "[![", "```", "<img", "<div", "</div", "<p", "</p")):
            return None
        if re.fullmatch(r"<br\s*/?>", x, flags=re.I):
            return None
        # Uploaded-attachment links, badges and bare/link-heavy metadata are not descriptions.
        low = x.lower()
        if "user-attachments/" in low or "img.shields.io/" in low:
            return None
        if x.startswith("[") and "](" in x and x.count("](") >= 1:
            return None
        if x.startswith(">"):
            x = re.sub(r"^>\s?", "", x)
        clean = strip_md(x)
        if not clean:
            return None
        # Avoid section labels / fragments.
        if clean.endswith(":") or len(clean) < 20:
            return None
        return clean

    for line in lines:
        clean = usable(line)
        if clean:
            paragraph.append(clean)
            # A real sentence/paragraph is enough; don't consume the whole README.
            joined = " ".join(paragraph)
            if len(joined) >= 40:
                return joined[:360].rstrip()
        elif paragraph:
            joined = " ".join(paragraph).strip()
            if len(joined) >= 24:
                return joined[:360].rstrip()
            paragraph = []

    if paragraph:
        joined = " ".join(paragraph).strip()
        if len(joined) >= 24:
            return joined[:360].rstrip()

    return "Documentation, source and usage information for this G'MIC filter."

def discover_filters():
    items=[]
    for folder in sorted(ROOT.iterdir(),key=lambda p:p.name.casefold()):
        if not folder.is_dir() or folder.name in IGNORE_DIRS: continue
        r=folder/"README.md"
        if not r.is_file(): continue
        text=r.read_text(encoding="utf-8",errors="replace")
        h=re.search(r"^#\\s+(.+?)\\s*$",text,flags=re.M)
        title=clean_title(h.group(1)) if h else folder.name.replace("-"," ").title()
        desc=first_description(text,h.end() if h else 0)
        items.append((folder.name,title,desc))
    return items

def render_filter(folder,title,desc):
    folder=html.escape(folder,quote=True); title=html.escape(title); desc=html.escape(desc)
    return f"""<h3><a href="./{folder}/">{title}</a></h3>

<p>{desc}</p>

<sub><a href="./{folder}/">View filter →</a></sub>

<br><br>"""

def main():
    source=README.read_text(encoding="utf-8")
    if START not in source or END not in source:
        raise SystemExit("README.md is missing the filter-index markers.")
    before,rest=source.split(START,1); _,after=rest.split(END,1)
    items=discover_filters()
    index="\n\n".join(render_filter(*x) for x in items) if items else "<p><em>No filters found.</em></p>"
    rendered=before+START+"\n\n"+index+"\n\n"+END+after
    if rendered!=source: README.write_text(rendered,encoding="utf-8")

if __name__=="__main__": main()

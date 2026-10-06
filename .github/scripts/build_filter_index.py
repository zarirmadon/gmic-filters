from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START = "<!-- FILTER_INDEX_START -->"
END = "<!-- FILTER_INDEX_END -->"

ASSET_DIR = ROOT / ".github" / "assets" / "icons"
POOL_DIR = ASSET_DIR / "breeze"
ASSIGNMENTS_FILE = ASSET_DIR / "assignments.json"
BREEZE_SOURCE = ROOT / ".breeze-icons"
IGNORE_DIRS = {".git", ".github", ".breeze-icons"}
POOL_SIZE = 100

# IMPORTANT: use Breeze's full 48px APPLICATION artwork first.
# This is the colourful family the user selected, not mimetype/status/action icons.
PRIMARY_DIR = BREEZE_SOURCE / "icons" / "apps" / "48"
FALLBACK_DIRS = [
    BREEZE_SOURCE / "icons" / "categories" / "32",
    BREEZE_SOURCE / "icons" / "places" / "48",
]

# Exclude obvious product/platform identities and unsuitable system symbols.
BLOCKED = (
    "adobe", "android", "apple", "blender", "chrome", "chromium", "discord",
    "dropbox", "facebook", "firefox", "github", "gitlab", "google", "inkscape",
    "krita", "libreoffice", "microsoft", "office", "opera", "skype", "spotify",
    "steam", "telegram", "thunderbird", "twitter", "ubuntu", "vlc", "whatsapp",
    "windows", "youtube", "gimp", "kde-logo", "plasma-logo"
)


def clean_title(title):
    return re.sub(r"^[^\w'“\"]+\s*", "", title).strip()


def readable_first_paragraph(text, title_end):
    """Find the first genuinely readable prose paragraph after the H1."""
    remainder = text[title_end:]

    # Remove comments and common standalone HTML spacing/image lines.
    remainder = re.sub(r"<!--.*?-->", "", remainder, flags=re.S)

    for block in re.split(r"\n\s*\n", remainder):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            continue
        if re.fullmatch(r"<br\s*/?>", block, flags=re.I):
            continue
        if block.startswith("![") or block.startswith("<img"):
            continue
        if block.startswith("[!["):  # badge block
            continue

        if block.startswith(">"):
            block = re.sub(r"^>\s?", "", block, flags=re.MULTILINE)

        block = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", block)
        block = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", block)
        block = re.sub(r"<[^>]+>", "", block)
        block = block.replace("**", "").replace("__", "").replace("`", "")
        block = " ".join(block.split()).strip()

        # Reject fragments that are clearly not prose.
        if len(block) < 24:
            continue

        return block

    return ""


def collect_icon_candidates():
    if not PRIMARY_DIR.exists():
        raise SystemExit(
            "Breeze icons/apps/48 was not found. "
            "The workflow should have checked out KDE/breeze-icons."
        )

    found = {}

    # Full colourful application artwork gets absolute priority.
    for directory in [PRIMARY_DIR] + FALLBACK_DIRS:
        if not directory.exists():
            continue
        for svg in sorted(directory.glob("*.svg")):
            name = svg.stem.lower()
            if "symbolic" in name:
                continue
            if any(word in name for word in BLOCKED):
                continue
            found.setdefault(svg.stem, svg)

    if len(found) < POOL_SIZE:
        raise SystemExit(
            f"Only {len(found)} suitable full Breeze icons were found; "
            f"{POOL_SIZE} are required."
        )

    # Stable shuffle so the pool isn't simply alphabetic.
    ordered = sorted(
        found.items(),
        key=lambda pair: hashlib.sha256(
            ("breeze-colour-pool:" + pair[0]).encode("utf-8")
        ).hexdigest()
    )
    return ordered[:POOL_SIZE]


def build_icon_pool():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    POOL_DIR.mkdir(parents=True, exist_ok=True)

    selected = collect_icon_candidates()
    wanted = set()
    pool = []

    for number, (name, source) in enumerate(selected, 1):
        dest_name = f"{number:03d}-{name}.svg"
        wanted.add(dest_name)
        dest = POOL_DIR / dest_name
        shutil.copyfile(source, dest)
        pool.append(dest)

    for old in POOL_DIR.glob("*.svg"):
        if old.name not in wanted:
            old.unlink()

    licence = BREEZE_SOURCE / "COPYING-ICONS"
    if licence.exists():
        shutil.copyfile(licence, ASSET_DIR / "BREEZE-LICENSE.txt")

    (ASSET_DIR / "BREEZE-CREDIT.md").write_text(
        "# KDE Breeze Icons\n\n"
        "The SVG files in `breeze/` are selected from the official KDE "
        "Breeze Icons project and retain their original licensing.\n\n"
        "Official project: https://invent.kde.org/frameworks/breeze-icons\n\n"
        "See `BREEZE-LICENSE.txt`.\n",
        encoding="utf-8",
    )
    return pool


def load_assignments():
    if not ASSIGNMENTS_FILE.exists():
        return {}
    try:
        value = json.loads(ASSIGNMENTS_FILE.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def assign_icons(folder_names, pool):
    old = load_assignments()
    valid = {p.name for p in pool}

    # Deliberately discard assignments to icons no longer in the new
    # colourful application-style pool.
    assignments = {
        folder: icon for folder, icon in old.items()
        if folder in folder_names and icon in valid
    }
    used = set(assignments.values())

    for folder in sorted(folder_names):
        if folder in assignments:
            continue

        start = int(
            hashlib.sha256(("filter:" + folder).encode("utf-8")).hexdigest(), 16
        ) % len(pool)

        chosen = None
        for offset in range(len(pool)):
            name = pool[(start + offset) % len(pool)].name
            if name not in used:
                chosen = name
                break

        if chosen is None:  # only after 100 filters
            chosen = pool[start].name

        assignments[folder] = chosen
        used.add(chosen)

    ASSIGNMENTS_FILE.write_text(
        json.dumps(assignments, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return assignments


def discover_filters():
    """Every first-level folder containing README.md is a filter entry."""
    filters = []

    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name in IGNORE_DIRS:
            continue

        readme = folder / "README.md"
        if not readme.exists():
            continue

        text = readme.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)

        # Do NOT drop a filter just because its README formatting is unusual.
        if match:
            title = clean_title(match.group(1))
            description = readable_first_paragraph(text, match.end())
        else:
            title = folder.name.replace("-", " ").title()
            description = readable_first_paragraph(text, 0)

        if not description:
            description = "G'MIC filter — open this folder for details, source and documentation."

        filters.append((folder.name, title, description))

    return filters


def render_entry(folder, title, description, icon_name):
    icon = f".github/assets/icons/breeze/{icon_name}".replace(" ", "%20")
    # No table: GitHub tables draw boxes. A left-floating image gives us a
    # clean mini-card, and clear=left prevents the next item colliding.
    return (
        f'<p>\n'
        f'  <img src="{icon}" width="52" height="52" align="left" alt="" />\n'
        f'  &nbsp;&nbsp;<strong><a href="./{folder}/">{title}</a></strong><br>\n'
        f'  &nbsp;&nbsp;{description}\n'
        f'</p>\n'
        f'<br clear="left">\n'
        f'<hr>'
    )


def main():
    pool = build_icon_pool()
    filters = discover_filters()
    assignments = assign_icons([f[0] for f in filters], pool)

    index = "\n\n".join(
        render_entry(folder, title, description, assignments[folder])
        for folder, title, description in filters
    )

    root = README.read_text(encoding="utf-8")
    if START not in root or END not in root:
        raise SystemExit("Root README.md is missing the filter-index markers.")

    before, rest = root.split(START, 1)
    _, after = rest.split(END, 1)

    README.write_text(
        before + START + "\n\n" + index + "\n\n" + END + after,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

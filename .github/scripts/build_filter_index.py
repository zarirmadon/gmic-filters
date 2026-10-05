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

# Prefer the colourful/general-purpose parts of Breeze rather than small
# monochrome action icons. Larger sizes are preferred where available.
CONTEXTS = ("mimetypes", "places", "devices", "categories", "status")
SIZES = ("64", "48", "32")

# Avoid names that are likely to be brands, applications, or unsuitable
# for a generic artistic-filter catalogue.
BLOCKED_WORDS = {
    "apple", "android", "chrome", "chromium", "firefox", "google",
    "microsoft", "windows", "ubuntu", "fedora", "debian", "arch",
    "dropbox", "skype", "steam", "spotify", "twitter", "facebook",
    "youtube", "github", "gitlab", "telegram", "discord", "whatsapp",
    "office", "libreoffice", "adobe", "photoshop", "gimp", "inkscape",
    "blender", "krita", "vlc", "konsole", "dolphin", "kate", "kdevelop",
    "plasma", "kde", "emblem-important", "dialog-error"
}

POOL_SIZE = 100


def clean_title(title):
    # Remove leading emoji/symbol decoration from child README H1.
    return re.sub(r"^[^\w'“\"]+\s*", "", title).strip()


def first_description(text, title_end):
    remainder = text[title_end:]
    for block in re.split(r"\n\s*\n", remainder):
        block = block.strip()
        if not block:
            continue
        if block.startswith("<br") or block.startswith("<!--") or block.startswith("#"):
            continue
        if block.startswith(">"):
            block = re.sub(r"^>\s?", "", block, flags=re.MULTILINE)

        # Keep readable link text but remove the URL.
        block = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", block)
        block = block.replace("**", "").replace("__", "").strip()

        # Strip simple HTML tags that may appear in the opening paragraph.
        block = re.sub(r"<[^>]+>", "", block).strip()

        if block:
            return " ".join(block.split())
    return ""


def candidate_icons():
    if not BREEZE_SOURCE.exists():
        raise SystemExit(
            "Official Breeze source was not found at .breeze-icons. "
            "The GitHub workflow should check it out automatically."
        )

    candidates = {}
    icons_root = BREEZE_SOURCE / "icons"

    # One version per icon name. Because sizes are processed largest first,
    # the first copy wins.
    for context in CONTEXTS:
        for size in SIZES:
            folder = icons_root / context / size
            if not folder.exists():
                continue

            for svg in sorted(folder.glob("*.svg")):
                stem_lower = svg.stem.lower()

                if any(word in stem_lower for word in BLOCKED_WORDS):
                    continue
                if "symbolic" in stem_lower:
                    continue

                candidates.setdefault(svg.stem, svg)

    # Deterministic but visually mixed selection rather than simply taking
    # the first 100 alphabetically.
    ordered = sorted(
        candidates.items(),
        key=lambda item: hashlib.sha256(item[0].encode("utf-8")).hexdigest()
    )

    if len(ordered) < POOL_SIZE:
        raise SystemExit(
            f"Only {len(ordered)} suitable Breeze icons were found; "
            f"{POOL_SIZE} are required."
        )

    return ordered[:POOL_SIZE]


def build_icon_pool():
    POOL_DIR.mkdir(parents=True, exist_ok=True)

    selected = candidate_icons()
    wanted = set()

    for number, (name, source) in enumerate(selected, start=1):
        dest_name = f"{number:03d}-{name}.svg"
        wanted.add(dest_name)
        shutil.copyfile(source, POOL_DIR / dest_name)

    # Remove obsolete pool SVGs if the selected official set changes.
    for old in POOL_DIR.glob("*.svg"):
        if old.name not in wanted:
            old.unlink()

    # Keep KDE's icon licence beside the copied assets.
    licence_source = BREEZE_SOURCE / "COPYING-ICONS"
    if licence_source.exists():
        shutil.copyfile(licence_source, ASSET_DIR / "BREEZE-LICENSE.txt")

    credit = ASSET_DIR / "BREEZE-CREDIT.md"
    credit.write_text(
        "# KDE Breeze Icons\n\n"
        "The SVG files in `breeze/` are selected from the official KDE "
        "Breeze Icons project and retain their original KDE licensing.\n\n"
        "Project: https://invent.kde.org/frameworks/breeze-icons\n\n"
        "See `BREEZE-LICENSE.txt` for the copied icon licence text.\n",
        encoding="utf-8"
    )

    return [POOL_DIR / f"{number:03d}-{name}.svg"
            for number, (name, _) in enumerate(selected, start=1)]


def load_assignments():
    if not ASSIGNMENTS_FILE.exists():
        return {}
    try:
        data = json.loads(ASSIGNMENTS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def assign_icons(filter_names, pool):
    assignments = load_assignments()
    valid_pool_names = {p.name for p in pool}

    # Drop assignments for filters that no longer exist or icons no longer
    # present in the official 100-icon pool.
    assignments = {
        folder: icon for folder, icon in assignments.items()
        if folder in filter_names and icon in valid_pool_names
    }

    used = set(assignments.values())

    for folder in sorted(filter_names):
        if folder in assignments:
            continue

        # Stable hash chooses a starting point, then linear probing finds
        # the next unused icon. Existing assignments never move.
        start = int(hashlib.sha256(folder.encode("utf-8")).hexdigest(), 16) % len(pool)

        chosen = None
        for offset in range(len(pool)):
            icon = pool[(start + offset) % len(pool)].name
            if icon not in used:
                chosen = icon
                break

        # Only possible after more than 100 filters.
        if chosen is None:
            chosen = pool[start].name

        assignments[folder] = chosen
        used.add(chosen)

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    ASSIGNMENTS_FILE.write_text(
        json.dumps(assignments, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )
    return assignments


def discover_filters():
    filters = []

    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name in IGNORE_DIRS:
            continue

        readme = folder / "README.md"
        if not readme.exists():
            continue

        text = readme.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
        if not match:
            continue

        title = clean_title(match.group(1))
        description = first_description(text, match.end())

        if title and description:
            filters.append((folder.name, title, description))

    return filters


def render_entry(folder, title, description, icon_name):
    icon_path = f".github/assets/icons/breeze/{icon_name}".replace(" ", "%20")

    # A compact two-column HTML table gives the icon enough visual weight
    # without creating the huge vertical gaps of the old catalogue.
    return (
        '<table><tr>\n'
        f'<td width="54" valign="top">'
        f'<img src="{icon_path}" width="42" height="42" alt=""></td>\n'
        f'<td valign="top"><strong><a href="./{folder}/">{title}</a></strong><br>\n'
        f'{description}</td>\n'
        '</tr></table>'
    )


def main():
    pool = build_icon_pool()
    filters = discover_filters()
    filter_names = [folder for folder, _, _ in filters]
    assignments = assign_icons(filter_names, pool)

    entries = [
        render_entry(folder, title, description, assignments[folder])
        for folder, title, description in filters
    ]
    index = "\n\n".join(entries)

    root_text = README.read_text(encoding="utf-8")

    if START not in root_text or END not in root_text:
        raise SystemExit(
            "Root README.md is missing "
            "<!-- FILTER_INDEX_START --> and <!-- FILTER_INDEX_END -->."
        )

    before, rest = root_text.split(START, 1)
    _, after = rest.split(END, 1)

    README.write_text(
        before + START + "\n\n" + index + "\n\n" + END + after,
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()

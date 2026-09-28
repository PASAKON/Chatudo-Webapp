#!/usr/bin/env python3
"""Chatudo site checker. Stdlib only, no network.

Fails (non-zero exit) if any of the following is true anywhere in
public/**/*.html:
  1. a required page is missing from public/
  2. an internal link (href/src) points at a file or in-page anchor
     that does not exist
  3. the text "—" (em dash) appears anywhere in the file
  4. any <script> tag is present
  5. any emoji codepoint appears in the file text
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

REQUIRED_PAGES = [
    "index.html",
    "pricing/index.html",
    "privacy/index.html",
    "terms/index.html",
    "data-deletion/index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
]

EM_DASH = "—"

SCRIPT_TAG_RE = re.compile(r"<script\b", re.IGNORECASE)
LINK_ATTR_RE = re.compile(r'(?:href|src)="([^"]*)"')
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')

# Emoji / pictograph / dingbat / arrow ranges. This also covers the
# characters the brief calls out by name: check mark U+2713, multiplication
# x U+2715 and rightwards arrow U+2192 all fall in ←-➿ below.
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F000-\U0001FFFF"  # all supplementary-plane emoji blocks
    "←-⇿"  # arrows
    "⌀-⏿"  # misc technical (hourglass, timer, etc.)
    "■-➿"  # geometric shapes, misc symbols, dingbats (incl. ✓ ✕)
    "⬀-⯿"  # misc symbols and arrows
    "️"  # variation selector-16
    "‍"  # zero width joiner (emoji sequences)
    "]"
)


def fail(errors):
    for e in errors:
        print(f"FAIL: {e}")
    print(f"\n{len(errors)} check(s) failed.")
    sys.exit(1)


def resolve_target(src_file: pathlib.Path, raw: str):
    """Return (path_to_check, fragment) for a href/src value, or None if
    the link is external / not checkable (http(s), mailto, tel, data)."""
    if raw.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
        return None
    if raw == "":
        return None
    path_part, _, fragment = raw.partition("#")
    if path_part == "":
        # pure same-page fragment, e.g. href="#contact"
        return (src_file, fragment or None)
    if path_part.startswith("/"):
        target = PUBLIC / path_part.lstrip("/")
    else:
        target = (src_file.parent / path_part).resolve()
    if str(target).endswith("/") or target.is_dir():
        target = target / "index.html" if target.is_dir() or not target.suffix else target
    elif target.suffix == "":
        target = target / "index.html"
    return (target, fragment or None)


def main():
    errors = []

    # 1. required pages
    for rel in REQUIRED_PAGES:
        if not (PUBLIC / rel).is_file():
            errors.append(f"missing required page: public/{rel}")

    if errors:
        fail(errors)

    html_files = sorted(PUBLIC.rglob("*.html"))
    if not html_files:
        fail(["no HTML files found in public/"])

    file_text = {f: f.read_text(encoding="utf-8") for f in html_files}
    file_ids = {f: set(ID_ATTR_RE.findall(t)) for f, t in file_text.items()}

    for f, text in file_text.items():
        rel = f.relative_to(ROOT)

        # 3. em dash
        if EM_DASH in text:
            count = text.count(EM_DASH)
            errors.append(f"{rel}: contains em dash — ({count} occurrence(s))")

        # 4. script tags
        if SCRIPT_TAG_RE.search(text):
            errors.append(f"{rel}: contains a <script> tag (no scripts allowed)")

        # 5. emoji
        found = EMOJI_PATTERN.findall(text)
        if found:
            uniq = sorted(set(found))
            codepoints = ", ".join(f"U+{ord(c):04X}" for c in uniq)
            errors.append(f"{rel}: contains emoji/pictograph character(s): {codepoints}")

        # 2. internal links
        for raw in LINK_ATTR_RE.findall(text):
            resolved = resolve_target(f, raw)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.is_file():
                errors.append(f"{rel}: broken link -> {raw} (resolved to {target.relative_to(ROOT) if ROOT in target.parents else target})")
                continue
            if fragment:
                ids = file_ids.get(target)
                if ids is None:
                    ids = set(ID_ATTR_RE.findall(file_text.get(target, target.read_text(encoding='utf-8'))))
                if fragment not in ids:
                    errors.append(f"{rel}: broken anchor -> {raw} (no id=\"{fragment}\" in {target.relative_to(ROOT)})")

    if errors:
        fail(errors)

    print(f"OK: {len(REQUIRED_PAGES)} required pages present.")
    print(f"OK: {len(html_files)} HTML file(s) scanned, no em dash, no <script>, no emoji, no broken internal links/anchors.")


if __name__ == "__main__":
    main()

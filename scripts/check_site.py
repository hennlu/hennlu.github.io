#!/usr/bin/env python3
"""Static integrity checks for the academic website (standard library only)."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = [
    "index.html", "index-fr.html", "research.html", "research-fr.html",
    "publications.html", "publications-fr.html", "talks.html",
    "talks-fr.html", "teaching.html", "teaching-fr.html",
    "Teaching2026-2027.html", "anr.html", "anr-fr.html",
    "students.html", "students-fr.html", "cv.html", "cv-fr.html",
    "music.html", "music-fr.html", "404.html",
]
errors = []


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a", "link", "script", "img", "source"}:
            for field in ("href", "src"):
                if attrs.get(field):
                    self.links.append((tag, field, attrs[field]))
        if tag == "img":
            self.images.append(attrs)


def check_path(source: Path, target: str):
    target = target.strip()
    if not target or target.startswith(("#", "data:", "javascript:", "mailto:", "tel:")):
        return
    if "{{" in target or "{%" in target:
        return  # These resolve during Jekyll's Liquid rendering.
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return
    candidate = unquote(parsed.path)
    if not candidate:
        return
    if candidate.startswith("/"):
        path = ROOT / candidate.lstrip("/")
    else:
        path = source.parent / candidate
    if candidate.endswith("/"):
        path /= "index.html"
    if not path.resolve().is_relative_to(ROOT.resolve()):
        errors.append(f"{source.relative_to(ROOT)}: path escapes repository: {target}")
    elif not path.is_file():
        errors.append(f"{source.relative_to(ROOT)}: missing {target}")


for name in PRIMARY:
    if not (ROOT / name).is_file():
        errors.append(f"Required page missing: {name}")

layout = ROOT / "_layouts" / "default.html"
if not layout.is_file():
    errors.append("Shared Jekyll layout is missing")
elif 'name="viewport"' not in layout.read_text(encoding="utf-8"):
    errors.append("Shared layout needs a mobile viewport")

for page in ROOT.rglob("*.html"):
    if ".git" in page.parts or "_site" in page.parts:
        continue
    text = page.read_text(encoding="utf-8")
    parser = LinkParser()
    parser.feed(text)
    for _, _, target in parser.links:
        check_path(page, target)
    if page.name in PRIMARY:
        if not text.startswith("---\n"):
            errors.append(f"{page.relative_to(ROOT)}: expected Jekyll front matter")
        if not re.search(r"(?m)^description:", text):
            errors.append(f"{page.relative_to(ROOT)}: missing page description")
        if not re.search(r"(?m)^lang:", text):
            errors.append(f"{page.relative_to(ROOT)}: missing page language")
        for img in parser.images:
            if not img.get("alt"):
                errors.append(f"{page.relative_to(ROOT)}: image missing alt text")

for name in ["_data/publications.json", "robots.txt", "sitemap.xml", "favicon.svg", "cv2web.pdf"]:
    if not (ROOT / name).is_file():
        errors.append(f"Required resource missing: {name}")

pdf = ROOT / "cv2web.pdf"
if pdf.is_file() and not pdf.read_bytes().startswith(b"%PDF-"):
    errors.append("CV is not a valid PDF file header")

if errors:
    print(f"{len(errors)} site error(s):")
    for err in errors:
        print(" -", err)
    sys.exit(1)
print(f"OK: {len(PRIMARY)} core pages exist; all local HTML links resolve.")

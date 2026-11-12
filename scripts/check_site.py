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

# Talks archive: catch broken/mismatched abstracts and empty event links.
import json
from html import unescape

talks_archive = ROOT / "Talks.html"
talk_meta_path = ROOT / "_data" / "talk_metadata.json"
talk_layout = ROOT / "_layouts" / "talk-abstract.html"
if not talk_layout.is_file():
    errors.append("Shared talk abstract layout is missing")
if not talk_meta_path.is_file():
    errors.append("Talk abstract metadata is missing")
elif talks_archive.is_file():
    try:
        talk_meta = json.loads(talk_meta_path.read_text(encoding="utf-8"))
        archive_text = talks_archive.read_text(encoding="utf-8")
        if re.search(r'<a\\s+href=""', archive_text):
            errors.append("Talks.html contains empty links")
        entries = re.findall(r'<p class="talk-entry">([\\s\\S]*?)</p>', archive_text)
        seen_abstracts = set()
        for entry in entries:
            link = re.search(r'<a\\s+href="([^"]+)"[^>]*>abstract</a>', entry)
            if not link:
                continue
            target = unquote(link.group(1))
            key = Path(target).stem
            if key in seen_abstracts:
                errors.append(f"Talk abstract reused in multiple archive entries: {target}")
            seen_abstracts.add(key)
            meta = talk_meta.get(key)
            if not meta:
                errors.append(f"No metadata for talk abstract: {target}")
                continue
            archive_title = re.search(r'<i>([\\s\\S]*?)</i>', entry)
            if archive_title:
                normalized_title = " ".join(unescape(re.sub(r'<[^>]+>', '', archive_title.group(1))).split())
                if normalized_title != meta.get("title"):
                    errors.append(f"Title mismatch between Talks.html and {target}")
            page = ROOT / target
            if not page.is_file():
                errors.append(f"Talk abstract page missing: {target}")
            else:
                content = page.read_text(encoding="utf-8")
                if "layout: talk-abstract" not in content or f'talk_key: "{key}"' not in content:
                    errors.append(f"Talk page does not use shared layout/metadata: {target}")
        for key, meta in talk_meta.items():
            if not (ROOT / f"{key}.html").is_file():
                errors.append(f"Orphaned talk metadata, page missing: {key}.html")
            if not meta.get("title") or not meta.get("date"):
                errors.append(f"Missing title/date for talk: {key}")
            for resource in meta.get("resources", []):
                if resource.get("url"):
                    check_path(talks_archive, resource["url"])
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid talk metadata: {exc}")

if errors:
    print(f"{len(errors)} site error(s):")
    for err in errors:
        print(" -", err)
    sys.exit(1)
print(f"OK: {len(PRIMARY)} core pages exist; all local HTML links resolve.")

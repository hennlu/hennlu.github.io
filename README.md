# Lucien Hennecart — academic website

Source of the public academic website at https://hennlu.github.io/.

## Editing

- The primary pages use the Jekyll layout `_layouts/default.html` and `styles.css`.
- Research papers are stored in `_data/publications.json`. Update a record once to update the English and French publication lists.
- English and French primary pages live in the repository root (`index.html`, `index-fr.html`, etc.).
- Archive URLs and existing talks/lecture PDFs are intentionally retained to avoid breaking external links.
- The current HTML CV (`cv.html`, `cv-fr.html`) and its printable PDF (`cv2web.pdf`) describe the CNRS appointment and the 2026 publication list. Update both versions when CV details change.
- Keep research announcements factual and avoid claiming recruitment is open until an official call exists.
- The archive `Talks.html` retains older abstracts and slides; `talks.html` is the new overview. Its five most recent talks are shown on both `talks.html` and `talks-fr.html` from `_data/recent_talks.json`, through `_includes/recent-talks.html`. When adding a talk to the archive, also add its metadata to that JSON file so the recent-talks preview stays current; entries are sorted by `date` and only the five newest are displayed. Unused legacy PHP templates and drafts are stored under `_archive/legacy/` and excluded from the published site.

## Testing

Run `python3 scripts/check_site.py` to inspect local URLs, page metadata and required core pages. A GitHub Actions workflow runs these checks **and performs a Jekyll build** for pull requests.

## Updating

Create a branch, edit the pages, check links, open a pull request, merge after review. GitHub Pages builds Jekyll on the main branch. Avoid renaming or moving established PDF links.

# Lucien Hennecart — academic website

Source of the public academic website at https://hennlu.github.io/.

## Editing

- The primary pages use the Jekyll layout `_layouts/default.html` and `styles.css`.
- Research papers are stored in `_data/publications.json`. Update a record once to update the English and French publication lists.
- English and French primary pages live in the repository root (`index.html`, `index-fr.html`, etc.).
- Archive URLs and existing talks/lecture PDFs are intentionally retained to avoid breaking external links.
- The old `cv2web.pdf` is an archive; the navigation points to the current `cv.html` until a refreshed official PDF is verified.
- Keep research announcements factual and avoid claiming recruitment is open until an official call exists.
- The archive `Talks.html` retains older abstracts and slides; `talks.html` is the new overview.

## Testing

Run `python3 scripts/check_site.py` to inspect local URLs, page metadata and required core pages. A GitHub Actions workflow does the same for pull requests.

## Updating

Create a branch, edit the pages, check links, open a pull request, merge after review. GitHub Pages builds Jekyll on the main branch. Avoid renaming or moving established PDF links.

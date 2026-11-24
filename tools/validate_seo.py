"""Check the public site's search metadata, sitemap, robots.txt and internal links.

Run from anywhere: python tools/validate_seo.py
It reads the files GitHub Pages publishes (the repository minus the paths that
_config.yml excludes) and exits non-zero with a list of problems.
"""

import datetime
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://astera.run"
REQUIRED_EXCLUDES = {"README.md", "docs/", "tools/", "content/"}
# Case-sensitive: the guide legitimately says "placeholders" when explaining command examples.
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|PLACEHOLDER)\b|[Ll]orem ipsum|\{\{|\}\}")
FORBIDDEN_SCHEMA = re.compile(r'"(aggregateRating|review|reviewRating)"')


def excludes():
    config = (ROOT / "_config.yml").read_text(encoding="utf-8")
    return [line.strip()[2:].strip() for line in config.splitlines() if line.strip().startswith("- ")]


def public_files():
    patterns = excludes()
    files = set()
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        parts = relative.split("/")
        if any(part.startswith((".", "_")) for part in parts):
            continue  # Jekyll skips dot and underscore paths (and .git).
        if any(relative == pattern or (pattern.endswith("/") and relative.startswith(pattern)) for pattern in patterns):
            continue
        files.add(relative)
    return files


def page_url(relative):
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]
    return "/" + relative


def resolve(path, files):
    """The file GitHub Pages serves for a URL path, or None."""
    path = path.lstrip("/")
    if path == "" or path.endswith("/"):
        candidate = path + "index.html"
        return candidate if candidate in files else None
    if path in files:
        return path
    if path + "/index.html" in files:
        return path + "/index.html"
    if path + ".html" in files:
        return path + ".html"
    return None


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.metas = {}
        self.canonicals = []
        self.alternates = []
        self.ids = set()
        self.references = []
        self.images = []
        self.h1 = 0
        self.json_ld = []
        self._title = None
        self._json = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "title":
            self._title = ""
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.metas.setdefault(key, []).append(attrs.get("content", ""))
        if tag == "link":
            rel = attrs.get("rel", "")
            if rel == "canonical":
                self.canonicals.append(attrs.get("href", ""))
            elif rel == "alternate" and "hreflang" in attrs:
                self.alternates.append((attrs["hreflang"], attrs.get("href", "")))
            elif "href" in attrs:
                self.references.append(("link", attrs["href"]))
        if tag in ("a", "use") and "href" in attrs:
            self.references.append((tag, attrs["href"]))
        if tag in ("img", "script", "source", "video", "iframe") and attrs.get("src"):
            self.references.append((tag, attrs["src"]))
        if tag == "video" and attrs.get("poster"):
            self.references.append((tag, attrs["poster"]))
        if tag == "img":
            self.images.append(attrs)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._json = ""

    def handle_endtag(self, tag):
        if tag == "title" and self._title is not None:
            self.titles.append(self._title.strip())
            self._title = None
        if tag == "script" and self._json is not None:
            self.json_ld.append(self._json)
            self._json = None

    def handle_data(self, data):
        if self._title is not None:
            self._title += data
        if self._json is not None:
            self._json += data

    def meta(self, key):
        values = self.metas.get(key, [])
        return values[0] if len(values) == 1 else None

    @property
    def indexable(self):
        return not any("noindex" in value for value in self.metas.get("robots", []))


def check():
    problems = []
    files = public_files()
    missing = REQUIRED_EXCLUDES - set(excludes())
    if missing:
        problems.append(f"_config.yml: must exclude {sorted(missing)} from the public site")

    pages = {}
    for relative in sorted(name for name in files if name.endswith(".html")):
        parser = Page()
        source = (ROOT / relative).read_text(encoding="utf-8")
        parser.feed(source)
        parser.source = source
        pages[relative] = parser

    link_count = 0
    for relative, page in pages.items():
        url = SITE + page_url(relative)
        visible = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", page.source, flags=re.S)
        if PLACEHOLDER.search(re.sub(r"<[^>]+>", " ", visible)):
            problems.append(f"{relative}: placeholder text ({PLACEHOLDER.search(re.sub(r'<[^>]+>', ' ', visible)).group(0)})")
        for image in page.images:
            if "alt" not in image or not image.get("width") or not image.get("height"):
                problems.append(f"{relative}: <img src={image.get('src')}> needs alt, width and height")
        for block in page.json_ld:
            try:
                json.loads(block)
            except json.JSONDecodeError as error:
                problems.append(f"{relative}: JSON-LD does not parse ({error})")
            if FORBIDDEN_SCHEMA.search(block):
                problems.append(f"{relative}: JSON-LD must not contain ratings or reviews")
        for tag, reference in page.references:
            target = urlsplit(urljoin(url, reference))
            if target.scheme not in ("http", "https") or target.netloc not in ("astera.run", "www.astera.run"):
                continue
            link_count += 1
            served = resolve(target.path, files)
            if served is None:
                problems.append(f"{relative}: broken link {reference}")
                continue
            if relative == "404.html" and tag != "use" and not reference.startswith(("/", "#", "https://")):
                problems.append(f"404.html: {reference} must be root-relative because the page is served at any path")
            if target.fragment and served in pages and target.fragment not in pages[served].ids:
                problems.append(f"{relative}: {reference} points to a missing anchor")

        if not page.indexable:
            continue
        if not page.lang:
            problems.append(f"{relative}: <html> needs lang")
        if len(page.titles) != 1 or not page.titles[0]:
            problems.append(f"{relative}: needs exactly one non-empty <title>")
        if not page.meta("description"):
            problems.append(f"{relative}: needs one meta description")
        if page.h1 != 1:
            problems.append(f"{relative}: needs exactly one <h1> (found {page.h1})")
        if len(page.canonicals) != 1:
            problems.append(f"{relative}: needs exactly one canonical link")
            continue
        canonical = page.canonicals[0]
        if not canonical.startswith(SITE + "/") or resolve(urlsplit(canonical).path, files) != relative:
            problems.append(f"{relative}: canonical {canonical} is not this page's HTTPS URL")
        for key in ("og:title", "og:description", "og:image", "og:image:alt", "twitter:card"):
            if not page.meta(key):
                problems.append(f"{relative}: needs {key}")
        if page.meta("og:url") != canonical:
            problems.append(f"{relative}: og:url must equal the canonical URL")
        image = page.meta("og:image") or ""
        if not image.startswith(SITE + "/") or resolve(urlsplit(image).path, files) is None:
            problems.append(f"{relative}: og:image {image} is not a published file")

    indexable = {relative: page for relative, page in pages.items() if page.indexable and len(page.canonicals) == 1}
    by_canonical = {page.canonicals[0]: relative for relative, page in indexable.items()}
    for field in ("title", "description"):
        seen = {}
        for relative, page in indexable.items():
            value = page.titles[0] if field == "title" and page.titles else page.meta("description")
            if value in seen:
                problems.append(f"{relative}: {field} duplicates {seen[value]}")
            seen[value] = relative
    for relative, page in indexable.items():
        if not page.alternates:
            continue
        group = dict(page.alternates)
        if group.get(page.lang) != page.canonicals[0]:
            problems.append(f"{relative}: hreflang must include itself as {page.lang}")
        if "x-default" not in group:
            problems.append(f"{relative}: hreflang group needs x-default")
        for language, href in page.alternates:
            other = by_canonical.get(href)
            if other is None:
                problems.append(f"{relative}: hreflang {language} points to {href}, which is not an indexable canonical page")
            elif language != "x-default" and dict(indexable[other].alternates) != group:
                problems.append(f"{relative}: hreflang group differs from {other} (must be reciprocal)")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    except ET.ParseError as error:
        problems.append(f"sitemap.xml: not valid XML ({error})")
        sitemap = None
    if sitemap is not None:
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = []
        today = datetime.date.today()
        for entry in sitemap.findall("s:url", namespace):
            location = entry.findtext("s:loc", default="", namespaces=namespace)
            locations.append(location)
            if location not in by_canonical:
                problems.append(f"sitemap.xml: {location} is not an indexable canonical page")
            modified = entry.findtext("s:lastmod", default="", namespaces=namespace)
            try:
                if datetime.date.fromisoformat(modified) > today:
                    problems.append(f"sitemap.xml: {location} lastmod {modified} is in the future")
            except ValueError:
                problems.append(f"sitemap.xml: {location} lastmod {modified!r} is not a date")
        if len(locations) != len(set(locations)):
            problems.append("sitemap.xml: duplicate URLs")
        for canonical, relative in by_canonical.items():
            if canonical not in locations:
                problems.append(f"sitemap.xml: missing {canonical} ({relative})")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {SITE}/sitemap.xml" not in robots:
        problems.append("robots.txt: must point to the sitemap")
    if re.search(r"^Disallow:\s*/\s*$", robots, re.M):
        problems.append("robots.txt: blocks the whole site")
    if "404.html" not in pages or pages["404.html"].indexable:
        problems.append("404.html: must exist and be noindex")
    return problems, len(pages), len(indexable), link_count


def main():
    problems, page_count, indexable_count, link_count = check()
    if problems:
        print("\n".join(problems))
        print(f"{len(problems)} problem(s) found.")
        sys.exit(1)
    print(f"SEO checks passed: {page_count} pages ({indexable_count} indexable), {link_count} internal links and anchors.")


if __name__ == "__main__":
    main()

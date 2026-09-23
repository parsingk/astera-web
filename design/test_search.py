import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.robotparser import RobotFileParser
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://astera.run/"
PAGES = {
    "index.html": SITE,
    "guide.html": SITE + "guide.html",
    "index.ko.html": SITE + "index.ko.html",
    "guide.ko.html": SITE + "guide.ko.html",
}


class Page(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.metas = []
        self.links = []
        self.scripts = []
        self.text = []
        self.language = None
        self.in_script = False
        self.in_body = False
        self.resources = []
        source = ROOT / filename
        if not source.is_file():
            raise AssertionError(f"Expected public page: {filename}")
        self.feed(source.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.resources.append(attrs[attribute])
        if tag == "html":
            self.language = attrs.get("lang")
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_script = True
        elif tag == "body":
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        elif tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_script:
            self.scripts.append(json.loads(data))
        elif self.in_body:
            self.text.append(data)

    def meta(self, key, value):
        return next((meta.get("content") for meta in self.metas if meta.get(key) == value), None)

    def links_for(self, relation):
        return [link for link in self.links if link.get("rel") == relation]


class SearchVisibilityTests(unittest.TestCase):
    def test_public_pages_have_clear_indexing_and_share_signals(self):
        for filename, url in PAGES.items():
            with self.subTest(filename=filename):
                page = Page(filename)
                self.assertTrue(page.links_for("canonical"))
                self.assertEqual(page.links_for("canonical")[0]["href"], url)
                description = page.meta("name", "description")
                self.assertIsNotNone(description)
                self.assertGreater(len(description), 70)
                self.assertEqual(page.meta("property", "og:url"), url)
                self.assertEqual(page.meta("name", "twitter:card"), "summary_large_image")
                self.assertEqual(page.meta("property", "og:image"), SITE + "assets/banner.jpg")
                alternates = {link["hreflang"]: link["href"] for link in page.links_for("alternate")}
                self.assertEqual(alternates["en"], PAGES["guide.html" if "guide" in filename else "index.html"])
                self.assertEqual(alternates["ko"], PAGES["guide.ko.html" if "guide" in filename else "index.ko.html"])

    def test_korean_pages_expose_korean_text_without_javascript(self):
        home = Page("index.ko.html")
        guide = Page("guide.ko.html")
        self.assertEqual(home.language, "ko")
        self.assertEqual(guide.language, "ko")
        self.assertIn("작업 공간", " ".join(home.text))
        self.assertIn("첫 세션", " ".join(guide.text))
        for filename in ("index.ko.html", "guide.ko.html"):
            with self.subTest(filename=filename):
                markup = (ROOT / filename).read_text(encoding="utf-8")
                self.assertTrue("</title>" in markup, "Missing title closing tag")
                self.assertTrue("</main>" in markup, "Missing main closing tag")

    def test_home_describes_the_real_free_desktop_app(self):
        for filename in ("index.html", "index.ko.html"):
            with self.subTest(filename=filename):
                apps = [item for item in Page(filename).scripts if item.get("@type") == "SoftwareApplication"]
                self.assertEqual(len(apps), 1)
                app = apps[0]
                self.assertEqual(app["name"], "Astera")
                self.assertEqual(app["applicationCategory"], "DeveloperApplication")
                self.assertEqual(app["offers"]["price"], "0")
                self.assertIn("Windows", app["operatingSystem"])
                self.assertIn("macOS", app["operatingSystem"])
                self.assertIn("Linux", app["operatingSystem"])

    def test_sitemap_lists_only_the_four_public_language_pages(self):
        sitemap = ROOT / "sitemap.xml"
        self.assertTrue(sitemap.is_file())
        tree = ElementTree.parse(sitemap)
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = {item.text for item in tree.iter(namespace + "loc")}
        self.assertEqual(urls, set(PAGES.values()))

    def test_every_search_and_ai_crawler_can_fetch_public_pages(self):
        robots = RobotFileParser()
        rules = ROOT / "robots.txt"
        self.assertTrue(rules.is_file())
        robots.parse(rules.read_text(encoding="utf-8").splitlines())
        for bot in ("Googlebot", "Google-Extended", "Bingbot", "OAI-SearchBot", "GPTBot", "Claude-SearchBot", "Claude-User", "ClaudeBot", "PerplexityBot", "UnknownBot"):
            for url in PAGES.values():
                with self.subTest(bot=bot, url=url):
                    self.assertTrue(robots.can_fetch(bot, url))

    def test_design_review_does_not_compete_with_public_pages(self):
        directive = Page("design/review.html").meta("name", "robots")
        self.assertIsNotNone(directive)
        self.assertIn("noindex", directive)

    def test_public_page_local_links_and_media_exist(self):
        for filename in PAGES:
            for resource in Page(filename).resources:
                url = urlsplit(resource)
                if url.scheme or url.netloc or not url.path:
                    continue
                path = ROOT / (url.path.lstrip("/") or "index.html")
                with self.subTest(page=filename, resource=resource):
                    self.assertTrue(path.is_file(), f"Missing local resource: {resource}")


if __name__ == "__main__":
    unittest.main()

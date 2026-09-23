"""Build crawlable Korean pages from the site's existing translation catalog."""

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
SITE = "https://astera.run/"


def translations():
    source = (ROOT / "locales/ko.js").read_text(encoding="utf-8")
    match = re.search(r"const koreanMessages\s*=\s*(\{.*\})\s*;", source, re.S)
    if not match:
        raise ValueError("Could not find the Korean message catalog")
    return json.loads(match.group(1))


class KoreanPage(HTMLParser):
    def __init__(self, messages, page):
        super().__init__(convert_charrefs=False)
        self.messages = messages
        self.page = page
        self.parts = []
        self.skipped_depth = 0

    def attributes(self, tag, attrs, raw):
        attrs = dict(attrs)
        for marker, attribute in (
            ("data-i18n-content", "content"),
            ("data-i18n-aria-label", "aria-label"),
            ("data-i18n-href", "href"),
        ):
            key = attrs.get(marker)
            if key in self.messages:
                raw = re.sub(
                    rf'\b{re.escape(attribute)}="[^"]*"',
                    lambda _: f'{attribute}="{html.escape(self.messages[key], quote=True)}"',
                    raw,
                    count=1,
                )
        if tag == "html":
            raw = raw.replace('lang="en"', 'lang="ko"', 1)
            raw = raw.replace("<html", '<html data-static-language="ko"', 1)
        if tag == "link" and attrs.get("rel") == "canonical":
            raw = raw.replace(attrs["href"], SITE + self.page)
        if tag == "meta" and attrs.get("property") == "og:url":
            raw = raw.replace(attrs["content"], SITE + self.page)
        if tag == "meta" and attrs.get("property") == "og:locale":
            raw = raw.replace('content="en_US"', 'content="ko_KR"')
        return raw

    def handle_starttag(self, tag, attrs):
        if self.skipped_depth:
            if tag not in VOID_TAGS:
                self.skipped_depth += 1
            return
        raw = self.attributes(tag, attrs, self.get_starttag_text())
        self.parts.append(raw)
        key = dict(attrs).get("data-i18n")
        if key in self.messages:
            self.parts.append(self.messages[key])
            self.skipped_depth = 1

    def handle_startendtag(self, tag, attrs):
        if not self.skipped_depth:
            self.parts.append(self.attributes(tag, attrs, self.get_starttag_text()))

    def handle_endtag(self, tag):
        if self.skipped_depth:
            self.skipped_depth -= 1
            if not self.skipped_depth:
                self.parts.append(f"</{tag}>")
        else:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skipped_depth:
            self.parts.append(data)

    def handle_entityref(self, name):
        if not self.skipped_depth:
            self.parts.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skipped_depth:
            self.parts.append(f"&#{name};")

    def handle_comment(self, data):
        if not self.skipped_depth:
            self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def result(self):
        content = "".join(self.parts)
        content = re.sub(r'href="(index|guide)\.html', r'href="\1.ko.html', content)
        if self.page == "index.ko.html":
            content = content.replace(
                "Free, open-source desktop workspace for Claude Code and Codex with Smart Resume, account rolling, scheduled sessions, and orchestration Jobs.",
                "Claude Code와 Codex를 위한 무료 오픈소스 데스크톱 작업 공간. Smart Resume, 계정 자동 전환, 예약 실행과 오케스트레이션 Jobs를 제공합니다.",
            )
        return content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when generated pages are stale")
    args = parser.parse_args()
    messages = translations()
    stale = []
    for source, target in (("index.html", "index.ko.html"), ("guide.html", "guide.ko.html")):
        page = KoreanPage(messages, target)
        page.feed((ROOT / source).read_text(encoding="utf-8"))
        content = page.result()
        destination = ROOT / target
        if args.check:
            if not destination.is_file() or destination.read_text(encoding="utf-8") != content:
                stale.append(target)
        else:
            destination.write_text(content, encoding="utf-8")
    if stale:
        parser.error("stale Korean pages: " + ", ".join(stale))


if __name__ == "__main__":
    main()

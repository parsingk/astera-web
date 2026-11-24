"""Build the search landing pages, 404 page and sitemap from content/pages.json.

Each generated page is a page body in content/<locale>/<id>.html wrapped in the
site's shared header, metadata and footer. Existing hand-written pages
(index.html, guide.html and their generated Korean copies) are listed in the
registry only so the sitemap and footer links can include them.
"""

import argparse
import datetime
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "pages.json"
SITE = "https://astera.run"
ASSET_VERSION = "20261125-3"

ICONS = """  <svg class="icon-library" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 3v12m-4-4 4 4 4-4M5 15v5h14v-5"/></symbol>
    <symbol id="i-github" viewBox="0 0 24 24"><path d="M9 19c-4 1-4-2-6-2m12 5v-3.5c0-1 .1-1.7-.5-2.4 3-.3 6.2-1.5 6.2-6.7 0-1.5-.5-2.7-1.4-3.7.1-.4.6-1.8-.1-3.6 0 0-1.1-.4-3.8 1.4a13 13 0 0 0-7 0C5.8 1.7 4.7 2.1 4.7 2.1c-.7 1.8-.2 3.2-.1 3.6C3.7 6.7 3.2 8 3.2 9.4c0 5.2 3.2 6.4 6.2 6.7-.5.5-.7 1.3-.7 2.4V22"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></symbol>
    <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
    <symbol id="i-moon" viewBox="0 0 24 24"><path d="M20.8 13A9 9 0 0 1 11 3.2 9 9 0 1 0 20.8 13Z"/></symbol>
    <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
    <symbol id="i-external" viewBox="0 0 24 24"><path d="M14 3h7v7m0-7L10 14M10 3H4v17h17v-6"/></symbol>
  </svg>"""

UI = {
    "en": {
        "og_locale": "en_US",
        "skip": "Skip to content",
        "main_nav": "Main navigation",
        "mobile_nav": "Mobile navigation",
        "github": "View Astera on GitHub",
        "menu": "Open menu",
        "theme": "Switch to light theme",
        "theme_short": "Light theme",
        "home": "/",
        "guide": "/guide.html",
        "related": "Keep reading",
        "read": "Read",
        "cta_title": "Try Astera on your own project.",
        "cta_body": "Astera is free and open source (Apache-2.0). It runs the Claude Code and Codex CLIs you already use, so model usage stays on your own Anthropic or OpenAI plan.",
        "cta_download": "Download Astera",
        "cta_guide": "Read the guide",
        "platforms": "Windows 10/11 · macOS 12+ · Ubuntu 22.04+ / Debian 12+",
        "tagline": "Build beyond the stars.",
        "independent": "Astera is an independent open-source project. It is not made by or affiliated with Anthropic or OpenAI.",
        "note": "Made for people who build.",
        "groups": {"product": "Product", "providers": "Providers", "features": "Features",
                   "guides": "Guides", "compare": "Compare", "project": "Project"},
        "home_label": "Home",
        "guide_label": "Guide",
        "download_label": "Download",
        "changelog": "Changelog",
        "docs": "Docs",
        "docs_url": "https://github.com/parsingk/Astera#documentation",
        "english_only": "",
    },
    "ko": {
        "og_locale": "ko_KR",
        "skip": "본문으로 건너뛰기",
        "main_nav": "주 메뉴",
        "mobile_nav": "모바일 메뉴",
        "github": "GitHub에서 Astera 보기",
        "menu": "메뉴 열기",
        "theme": "라이트 테마로 전환",
        "theme_short": "라이트 테마",
        "home": "/index.ko.html",
        "guide": "/guide.ko.html",
        "related": "함께 읽기",
        "read": "읽기",
        "cta_title": "내 프로젝트에서 Astera를 써 보세요.",
        "cta_body": "Astera는 Apache-2.0 라이선스의 무료 오픈소스입니다. 지금 쓰는 Claude Code와 Codex CLI를 그대로 실행하므로 모델 사용량은 본인의 Anthropic 또는 OpenAI 요금제에서 차감됩니다.",
        "cta_download": "Astera 다운로드",
        "cta_guide": "가이드 읽기",
        "platforms": "Windows 10/11 · macOS 12+ · Ubuntu 22.04+ / Debian 12+",
        "tagline": "별 너머의 가능성을 만드세요.",
        "independent": "Astera는 Anthropic이나 OpenAI가 만들거나 제휴한 제품이 아닌 독립 오픈소스 프로젝트입니다.",
        "note": "만드는 사람들을 위해.",
        "groups": {"product": "제품", "providers": "지원 에이전트", "features": "기능",
                   "guides": "실전 가이드", "compare": "비교", "project": "프로젝트"},
        "home_label": "홈",
        "guide_label": "사용 가이드",
        "download_label": "다운로드",
        "changelog": "변경 내역",
        "docs": "문서",
        "docs_url": "https://github.com/parsingk/Astera/blob/main/README.ko.md#문서",
        "english_only": " (영어)",
    },
}

FOOTER_GROUPS = ("providers", "features", "guides", "compare")


def esc(value):
    return html.escape(value, quote=True)


def load_registry():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    pages = registry["pages"]
    ids = [page["id"] for page in pages]
    duplicates = {page_id for page_id in ids if ids.count(page_id) > 1}
    if duplicates:
        raise ValueError(f"duplicate page ids: {sorted(duplicates)}")
    for page in pages:
        datetime.date.fromisoformat(page["lastContentModified"])
        if page["locale"] not in UI:
            raise ValueError(f"{page['id']}: unsupported locale {page['locale']}")
    return pages


def output_file(path):
    """Map a public URL path to the file GitHub Pages serves for it."""
    if path.endswith("/"):
        return path.lstrip("/") + "index.html"
    return path.lstrip("/")


def published(pages):
    return [page for page in pages if page["status"] == "published"]


def translations(page, pages):
    """Published pages of the same translation group, including the page itself."""
    return [other for other in published(pages)
            if other["translationGroup"] == page["translationGroup"] and other.get("indexable", True)]


def localized(group, locale, pages):
    """The page of a translation group in a locale, or the English page as a fallback."""
    members = [page for page in published(pages) if page["translationGroup"] == group]
    exact = [page for page in members if page["locale"] == locale]
    return (exact or [page for page in members if page["locale"] == "en"] or [None])[0]


def theme_links(fragment):
    """Internal links keep the selected theme, the same way the existing pages do."""
    return re.sub(r'<a href="(/[^"]*)"(?![^>]*data-theme-link)', r'<a href="\1" data-theme-link', fragment)


def json_ld(page, url):
    kind = "TechArticle" if page["kind"] in ("guide", "comparison") else "WebPage"
    document = {
        "@type": kind,
        "@id": url + "#webpage",
        "url": url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": page["locale"],
        "isPartOf": {"@id": SITE + "/#website"},
        "about": {"@id": SITE + "/#app"},
        "dateModified": page["lastContentModified"],
        "breadcrumb": {"@id": url + "#breadcrumb"},
    }
    if kind == "TechArticle":
        document["headline"] = page["h1"]
    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Astera", "item": SITE + UI[page["locale"]]["home"]},
            {"@type": "ListItem", "position": 2, "name": page["navLabel"]},
        ],
    }
    data = {"@context": "https://schema.org", "@graph": [document, breadcrumb]}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def head(page, pages):
    ui = UI[page["locale"]]
    indexable = page.get("indexable", True)
    url = SITE + page["path"]
    image = page.get("socialImage", "/assets/banner.jpg")
    lines = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta name="description" content="{esc(page["description"])}">',
        '<meta name="theme-color" content="#0b1020">',
        f'<title>{esc(page["title"])}</title>',
    ]
    if indexable:
        lines.append(f'<link rel="canonical" href="{url}">')
        alternates = translations(page, pages)
        if len(alternates) > 1:
            for other in sorted(alternates, key=lambda item: item["locale"]):
                lines.append(f'<link rel="alternate" hreflang="{other["locale"]}" href="{SITE + other["path"]}">')
            default = next(other for other in alternates if other["locale"] == "en")
            lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE + default["path"]}">')
    else:
        lines.append('<meta name="robots" content="noindex">')
    lines += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Astera">',
        f'<meta property="og:title" content="{esc(page["title"])}">',
        f'<meta property="og:description" content="{esc(page["description"])}">',
    ]
    if indexable:
        lines.append(f'<meta property="og:url" content="{url}">')
    lines += [
        f'<meta property="og:image" content="{SITE + image}">',
        f'<meta property="og:image:width" content="{page.get("socialImageWidth", 1254)}">',
        f'<meta property="og:image:height" content="{page.get("socialImageHeight", 625)}">',
        f'<meta property="og:image:alt" content="{esc(page["socialImageAlt"])}">',
        f'<meta property="og:locale" content="{ui["og_locale"]}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(page["title"])}">',
        f'<meta name="twitter:description" content="{esc(page["description"])}">',
    ]
    if indexable:
        lines.append(f'<script type="application/ld+json">{json_ld(page, url)}</script>')
    lines += [
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" href="/assets/favicon-192.png" type="image/png" sizes="192x192">',
        '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">',
        '<link rel="preload" href="/assets/fonts/PublicSans-Regular.woff2" as="font" type="font/woff2" crossorigin>',
        "<script>\n    document.documentElement.dataset.theme = new URLSearchParams(location.search).get('theme') === 'light' ? 'light' : 'dark';\n  </script>",
        '<link rel="stylesheet" href="/styles.css">',
        '<link rel="stylesheet" href="/guide.css">',
        f'<link rel="stylesheet" href="/pages.css?v={ASSET_VERSION}">',
        f'<script src="/language.js?v={ASSET_VERSION}" defer></script>',
        f'<script src="/main.js?v={ASSET_VERSION}" defer></script>',
        '<script src="/downloads.js" defer></script>',
    ]
    return "\n".join("  " + line for line in lines)


def header(page, pages):
    ui = UI[page["locale"]]
    home, guide = ui["home"], ui["guide"]
    nav = (f'<a href="{home}#features" data-theme-link lang="en">Features</a>'
           f'<a href="{home}#workflow" data-theme-link lang="en">Workflow</a>'
           f'<a href="{guide}" data-theme-link lang="en">Guide</a>'
           f'<a href="{home}#faq" data-theme-link lang="en">FAQ</a>')
    language = ""
    if page.get("indexable", True):
        other_locale = "ko" if page["locale"] == "en" else "en"
        other = next((item for item in translations(page, pages) if item["locale"] == other_locale), None)
        if other:
            label = "한국어" if other_locale == "ko" else "English"
            hint = "한국어로 보기" if other_locale == "ko" else "View in English"
            language = (f'<a class="language-link" href="{other["path"]}" data-theme-link hreflang="{other_locale}" '
                        f'lang="{other_locale}" title="{hint}">{label}</a>\n        ')
    return f"""  <a class="skip-link" href="#main">{ui["skip"]}</a>
  <header class="site-header">
    <div class="nav-shell">
      <a class="brand" href="{home}" data-theme-link aria-label="Astera home"><img src="/assets/astera-mark.png" width="34" height="34" alt=""><span>Astera</span></a>
      <nav class="desktop-nav" aria-label="{ui["main_nav"]}">
        {nav}
      </nav>
      <div class="nav-actions">
        {language}<a class="github-link" href="https://github.com/parsingk/Astera" target="_blank" rel="noopener noreferrer" aria-label="{ui["github"]}"><svg class="icon"><use href="#i-github"/></svg><span>GitHub</span></a>
        <button class="icon-button theme-toggle theme-toggle-header" type="button" aria-label="{ui["theme"]}" aria-pressed="true"><svg class="icon"><use href="#i-sun"/></svg><span class="sr-only">{ui["theme_short"]}</span></button>
        <a class="button button-small button-ink" href="https://github.com/parsingk/Astera/releases/latest" target="_blank" rel="noopener noreferrer" data-download lang="en">Download <svg class="icon small"><use href="#i-download"/></svg></a>
        <button class="icon-button menu-toggle" type="button" aria-label="{ui["menu"]}" aria-expanded="false" aria-controls="mobile-nav"><svg class="icon"><use href="#i-menu"/></svg></button>
      </div>
    </div>
    <nav class="mobile-nav" id="mobile-nav" aria-label="{ui["mobile_nav"]}" hidden>{nav}</nav>
  </header>"""


def link_to(target, locale):
    """A link to another page, marked when the reader's language is unavailable."""
    suffix = UI[locale]["english_only"] if target["locale"] != locale else ""
    language = f' hreflang="{target["locale"]}"' if target["locale"] != locale else ""
    return f'<a href="{target["path"]}" data-theme-link{language}>{esc(target["navLabel"])}{suffix}</a>'


def related(page, pages):
    if not page.get("related"):
        return ""
    ui = UI[page["locale"]]
    links = []
    for group in page["related"]:
        target = localized(group, page["locale"], pages)
        if target is None:
            raise ValueError(f"{page['id']}: related page {group} is not published")
        suffix = ui["english_only"] if target["locale"] != page["locale"] else ""
        links.append(f'<a href="{target["path"]}" data-theme-link><span>{esc(target["navLabel"])}{suffix}</span>'
                     f'<span>{ui["read"]} <svg class="icon small"><use href="#i-arrow"/></svg></span></a>')
    return (f'\n      <nav class="feature-map page-related" aria-labelledby="related-title">\n'
            f'        <h2 id="related-title">{ui["related"]}</h2>\n        ' + "\n        ".join(links) + "\n      </nav>")


def call_to_action(page):
    if not page.get("cta", True):
        return ""
    ui = UI[page["locale"]]
    return f"""
      <div class="guide-finish page-cta">
        <div><h2>{ui["cta_title"]}</h2><p>{ui["cta_body"]}</p><p class="page-platforms">{ui["platforms"]}</p></div>
        <div class="page-cta-actions"><a class="button button-primary" href="https://github.com/parsingk/Astera/releases/latest" target="_blank" rel="noopener noreferrer" data-download><svg class="icon"><use href="#i-download"/></svg> {ui["cta_download"]}</a><a class="text-button" href="{ui["guide"]}" data-theme-link>{ui["cta_guide"]} <svg class="icon small"><use href="#i-arrow"/></svg></a></div>
      </div>"""


def footer(page, pages):
    ui = UI[page["locale"]]
    groups = []
    product = [f'<a href="{ui["home"]}" data-theme-link>{ui["home_label"]}</a>',
               f'<a href="{ui["guide"]}" data-theme-link>{ui["guide_label"]}</a>',
               f'<a href="https://github.com/parsingk/Astera/releases/latest" target="_blank" rel="noopener noreferrer" data-download>{ui["download_label"]}</a>',
               f'<a href="https://github.com/parsingk/Astera/releases" target="_blank" rel="noopener noreferrer">{ui["changelog"]}</a>']
    groups.append(("product", product))
    for group in FOOTER_GROUPS:
        members = []
        for item in pages:
            if item.get("footerGroup") != group or item["locale"] != "en" or item["status"] != "published":
                continue
            members.append(link_to(localized(item["translationGroup"], page["locale"], pages), page["locale"]))
        if members:
            groups.append((group, members))
    project = ['<a href="https://github.com/parsingk/Astera" target="_blank" rel="noopener noreferrer">GitHub</a>',
               f'<a href="{ui["docs_url"]}" target="_blank" rel="noopener noreferrer">{ui["docs"]}</a>',
               '<a href="https://github.com/parsingk/Astera/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">Apache-2.0</a>']
    groups.append(("project", project))
    columns = "\n".join(
        f'      <div><p class="footer-group-title">{ui["groups"][name]}</p>{"".join(links)}</div>'
        for name, links in groups)
    return f"""  <footer class="site-footer container">
    <div><a class="brand" href="{ui["home"]}" data-theme-link><img src="/assets/astera-mark.png" width="28" height="28" alt=""><span>Astera</span></a><p>{ui["tagline"]}</p></div>
    <nav class="footer-groups" aria-label="Astera">
{columns}
    </nav>
    <p class="footer-note">{ui["independent"]} {ui["note"]}</p>
  </footer>"""


def render(page, pages):
    ui = UI[page["locale"]]
    body = theme_links((ROOT / page["body"]).read_text(encoding="utf-8").strip())
    breadcrumb = (f'<p class="guide-breadcrumb"><a href="{ui["home"]}" data-theme-link>Astera</a>'
                  f'<span>/</span>{esc(page["section"])}</p>')
    lead = f'\n        <p class="guide-lead">{page["lead"]}</p>' if page.get("lead") else ""
    return f"""<!doctype html>
<html lang="{page["locale"]}" data-static-language="{page["locale"]}">
<head>
{head(page, pages)}
</head>
<body class="guide-page search-page">
{ICONS}

{header(page, pages)}

  <main id="main" class="container page-main">
    <article class="page-article">
      <header class="guide-intro guide-section page-intro">
        {breadcrumb}
        <h1>{esc(page["h1"])}</h1>{lead}
      </header>
{body}
{call_to_action(page)}{related(page, pages)}
    </article>
  </main>

{footer(page, pages)}
</body>
</html>
"""


def sitemap(pages):
    entries = []
    for page in published(pages):
        if not page.get("indexable", True):
            continue
        entries.append(f'  <url><loc>{SITE + page["path"]}</loc><lastmod>{page["lastContentModified"]}</lastmod></url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n")


def outputs(pages):
    files = {"sitemap.xml": sitemap(pages)}
    for page in published(pages):
        if page.get("body"):
            files[output_file(page["path"])] = render(page, pages)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail when generated files are stale")
    args = parser.parse_args()
    pages = load_registry()
    stale = []
    for name, content in outputs(pages).items():
        destination = ROOT / name
        if args.check:
            if not destination.is_file() or destination.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        parser.error("stale generated files: " + ", ".join(stale))


if __name__ == "__main__":
    main()

# Astera website

Astera's promotional website at [astera.run](https://astera.run), with dark and light themes, original product imagery, and English and Korean copy. Plain HTML, CSS, and JavaScript; no package installation or runtime build step.

## Preview

From `D:\parsingk\astera-web`:

```powershell
python -m http.server 5173 --bind 127.0.0.1
```

Open http://127.0.0.1:5173. `index.html` can also be opened directly for a basic offline preview.

Direct previews: [dark](http://127.0.0.1:5173/?theme=dark) and [light](http://127.0.0.1:5173/?theme=light). The header and footer theme buttons update the URL, so the selected theme survives a reload and can be shared as a link. Without a theme parameter, the page and design review open in dark mode. Only `?theme=light` explicitly selects light mode.

[Design review](http://127.0.0.1:5173/design/review.html) offers 1440, 768, 390, and 320px viewports plus layout and interaction checks. This review page needs the HTTP server. Saved previews: [desktop](design/desktop.png) and [mobile](design/mobile-review.png).

Run `node design/downloads.test.cjs` to check OS-specific installer selection, fallback behavior, and the download buttons on both pages.

The review page also has Light/Dark controls. [Open the dark review](http://127.0.0.1:5173/design/review.html?theme=dark). Dark captures: [desktop](design/dark-desktop.png), [mobile](design/dark-mobile-review.png), and [features](design/dark-features-review.png).

The latest hero uses a near-black sky, soft nebula light, and small glowing stars. On devices with a fine pointer, the background layers follow the pointer at different depths and settle back when it leaves. The entrance animation finishes within five seconds; touch and reduced-motion preferences keep the scene still. It uses CSS, a local SVG, and `hero.js`, with no animation library or continuous JavaScript render loop. Latest captures: [space desktop](design/space-desktop.png), [mobile](design/space-mobile-review.png), [light theme](design/space-light-review.png).

## Languages

The first visit follows the browser's primary language: Korean for `ko`/`ko-KR`, English otherwise. The header and footer offer **한국어 / English** controls. Explicit URL language takes priority over a saved selection, followed by the browser language.

- [Korean home](http://127.0.0.1:5173/index.ko.html) · [Korean Guide](http://127.0.0.1:5173/guide.ko.html)
- [English home](http://127.0.0.1:5173/) · [English Guide](http://127.0.0.1:5173/guide.html)

Switching keeps the theme and URL anchor. On the English pages, it also keeps the reading position; switching from a static Korean page opens the corresponding English section. A manual selection is saved locally; when storage is blocked, switching and links still preserve the language through the URL. Browser tab titles, descriptions, image alternatives, and media controls are translated along with the body copy. Large display headings, the main feature-card titles, and the header navigation (including its mobile menu and Download button) stay in English in both languages; smaller instructional headings follow the selected language. The language controls still show the language you can switch to. Existing product screenshots and recordings retain their original content.

English stays in `index.html` and `guide.html`; `data-i18n` keys connect it to the bundled `locales/ko.js` catalog. `language.js` applies the catalog and handles preference selection. Dynamic labels in `main.js` use `siteI18n.text`. No translation service or runtime dependency is required.

For search crawlers and direct Korean links, `index.ko.html` and `guide.ko.html` contain the translated text in the HTML itself. Generate them after editing either English page or `locales/ko.js`:

```powershell
python tools/build_locales.py
python tools/build_locales.py --check
```

The generated pages keep the same interactive design. Their language switch links back to the English page; the English pages still choose the browser language on a first visit. Canonical URLs, `hreflang`, and the sitemap connect the four public pages. `robots.txt` allows all search and AI crawlers to fetch them. The design review is excluded from indexing. Search engines determine whether and when to index the site.

Run `python -m unittest discover -s design -p 'test_search.py' -v` to check these search signals, alongside the download-routing test above.

The design review includes Korean/English controls and **Check languages**. All 38 language checks passed, covering language selection, translated copy, English display headings, navigation, and storage restrictions. The bilingual layout review passed all 32 combinations (two pages × two languages × two themes × four widths); the interaction review passed 26 home / 30 Guide checks per language, including the hero's pointer response and reset. Earlier Korean captures, before the English-only header and inline GIFs: [home](design/ko-desktop.png), [Guide](design/ko-guide.png).

## Included

- Responsive landing page with real Astera screenshots and original icon.
- Product emphasis backed by the app's implementation: Smart Resume checkpoints, the Jobs dependency graph, `/astera-orchestration`, and local Host session continuity. The [positioning notes](docs/product-positioning.md) record sources and the limits of each claim.
- A [Guide](http://127.0.0.1:5173/guide.html) covering the first session, Terminal/Chat, history, account rolling, scheduling, Slack, Jobs, How It Works, workspace tools, and settings. Includes a responsive table of contents and the existing product demos.
- Terminal-first product preview with a Chat/Terminal switch and an enlarged screenshot dialog.
- Inline account rolling, scheduling, and Jobs GIF recordings from the app README, shown in the matching home cards and Guide sections. Every demo button opens its full video and starts playback immediately, with native controls available. GIFs load lazily; reduced-motion preferences select a still frame instead.
- FAQ, mobile navigation, and synchronized header/footer theme controls.
- Local fonts and media. Download buttons query the official GitHub release API for the latest installer.
- Download buttons that select the latest Windows installer, macOS disk image, or Linux AppImage from the official Astera GitHub release, plus documentation links to the repository.

The main navigation and footer link to the Guide. Moving between the landing page and Guide keeps the selected theme and language. The design review has Home/Guide controls for checking both pages at the same viewport sizes. Smart Resume, How It Works, and Agent browser have no experimental badge; the Guide explains how to enable each feature.

The latest product-emphasis update adds dedicated Smart Resume, orchestration-skill, and Host guides, and moves Optional features into the Work with Astera group. Its 38 browser language checks and static reference/translation checks passed. The full layout rerun stopped at a 30-second browser-helper timeout, so the layout and interaction results above describe the preceding iteration. Final visual captures of this content update are not yet available.

Initial Guide validation: 30 interaction checks passed; the landing page passed 22. Both pages were checked at 1440, 768, 390, and 320px in both themes. Saved images are from earlier landing-page iterations; a Guide capture was unavailable because the agent browser did not paint within its screenshot timeout.

Before localization, the expanded Guide passed all eight layout checks on 2026-09-22, with no overflow, missing images, or broken anchors. Background rendering limited some dynamic checks at that stage; see [design direction](docs/design-direction.md) for that history. The bilingual review above supersedes those results.

The [feature coverage review](docs/design-direction.md#기능-가이드-보강과-누락-검토--2026-09-22) maps the app's documented features to Guide sections. The How It Works walkthrough GIF and the existing Jobs GIF are included in the **Astera app README**, at `D:\parsingk\astera\README.md`.

The product screenshots are unchanged originals. Feature diagrams illustrate behavior; they are not screenshots. Download buttons read the latest GitHub release and link straight to the installer for the visitor’s OS. If the release cannot be checked or no matching file is available, they open the release page for manual selection. Linux defaults to the x86_64 AppImage. GitHub Pages serves the plain static files at `astera.run`.

See [design direction](docs/design-direction.md) for reference research, content boundaries, and review criteria.

## Asset provenance

Images, the icon, and videos were copied from `D:\parsingk\astera`. The original `rolling-demo.gif`, `schedule-demo.gif`, and `jobs-demo.gif` are unchanged copies of the recordings embedded in the app README. Each matching `*-demo-still.png` is its unmodified first frame, extracted for reduced-motion display. Public Sans was copied from the app's bundled fonts, with its OFL license in `assets/fonts/PublicSans-LICENSE.txt`.

`assets/starfield.svg` is an original vector illustration of stars created for this website; the surrounding nebula is drawn with CSS gradients.

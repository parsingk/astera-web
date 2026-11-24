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

- Astera 1.5.1–1.5.5 additions in both Guide languages: [shared Claude Code plugins](http://127.0.0.1:5173/guide.html#shared-plugins) for Claude and Codex accounts, the [Run report](http://127.0.0.1:5173/guide.html#run-report) with its pull request comment and Slack post, [external reviewers](http://127.0.0.1:5173/guide.html#reviewers) over ACP, Claude Code's [Windows shell in Codex's sandbox](http://127.0.0.1:5173/guide.html#sandbox-windows-claude), [Kubernetes](http://127.0.0.1:5173/guide.html#kubernetes) manifests and the live cluster view, and [pasting copied files as paths](http://127.0.0.1:5173/guide.html#paste-paths). The home Sandbox card reflects the Windows change.
- Astera 1.5.0 [agent setup and controls](http://127.0.0.1:5173/#agent-control), with bilingual guides for [shared MCP & Skills](http://127.0.0.1:5173/guide.html#mcp-skills), [agent profiles](http://127.0.0.1:5173/guide.html#agent-profiles), [Observe, Enforce, and Credentials](http://127.0.0.1:5173/guide.html#security-access), [sandbox coverage](http://127.0.0.1:5173/guide.html#sandbox), and [Findings](http://127.0.0.1:5173/guide.html#findings). Remote Runtime covers setup reports, expected extensions, controller identity, and pausing scheduled Jobs on unpairing. Jobs includes token totals and Audit Logs; sessions and settings cover the release's input and configuration fixes.
- Bilingual [GitHub lifecycle guide](http://127.0.0.1:5173/guide.html#github-lifecycle) and [landing overview](http://127.0.0.1:5173/#github-lifecycle): opt-in Jobs that push, open or bind draft PRs, follow CI, repair code failures, rerun infrastructure failures, ask for decisions, and obtain a second agent's review. Merge-ready tracks the current PR head and can be withdrawn; the user merges. Includes Settings → GitHub, CLI/MCP/SDK access, reconvergence, and Remote Runtime conditions. The sessions guide covers automatic tab closure for agent-started sessions.
- Bilingual [plugin guide](http://127.0.0.1:5173/guide.html#plugins) for folder/npm installation, permissions, settings, secrets, logs, and event/notification providers; [SDK and events](http://127.0.0.1:5173/guide.html#sdk) for Node.js integrations on the local Host.
- [Jobs from issues](http://127.0.0.1:5173/guide.html#job-sources) through the source picker, CLI, and MCP, with GitHub and plugin source requirements. [Plugin completion checks](http://127.0.0.1:5173/guide.html#completion-plugins) covers Task attachment, findings, repair, unavailable-check decisions, and Runtime installation. The workspace guide also covers terminal file/folder links.
- [Remote Runtime overview](http://127.0.0.1:5173/#remote-runtime) and bilingual [setup guide](http://127.0.0.1:5173/guide.html#remote-runtime): Settings-based pairing and revocation, remote Jobs and sessions, CLI/MCP targeting, and Host scheduling and restart conditions.
- [Creative Hub](http://127.0.0.1:5173/guide.html#creative-hub) for Higgsfield accounts, credits, workspaces, and user-chosen switching; [media viewer](http://127.0.0.1:5173/guide.html#media-viewer) and [agent app workspace](http://127.0.0.1:5173/guide.html#agent-app) explanations. Jobs covers git changes/diffs, and Host covers recovery without the app open.
- Headless CLI overview and bilingual [CLI guide](http://127.0.0.1:5173/guide.html#headless-cli): command installation, Host capabilities, sessions, skill-planned Jobs, progress and checks, user questions, and script exit codes. The guide explains setup, scheduling limits, and Host requirements.
- Bilingual [MCP overview](http://127.0.0.1:5173/#mcp) and [connection guide](http://127.0.0.1:5173/guide.html#mcp): local client registration, Jobs and checks, optional session and GitHub access, How It Works records, and token-protected HTTP for other devices. The guide states the access defaults and network limits.
- Responsive landing page with real Astera screenshots and original icon.
- Product emphasis backed by the app's implementation: Smart Resume checkpoints, the Jobs dependency graph, `/astera-orchestration`, and local Host session continuity. The [positioning notes](docs/product-positioning.md) record sources and the limits of each claim.
- A [Guide](http://127.0.0.1:5173/guide.html) covering the first session, Terminal/Chat, history, account rolling, scheduling, Slack, Jobs, How It Works, workspace tools, and settings. Includes a responsive table of contents and the existing product demos.
- Terminal-first product preview with a Chat/Terminal switch and an enlarged screenshot dialog.
- Inline account rolling, scheduling, and Jobs GIF recordings from the app README, shown in the matching home cards and Guide sections. Every demo button opens its full video and starts playback immediately, with native controls available. GIFs load lazily; reduced-motion preferences select a still frame instead.
- FAQ, mobile navigation, and synchronized header/footer theme controls.
- Local fonts and media. Download buttons query the official GitHub release API for the latest installer.
- Download buttons that select the latest Windows installer, macOS disk image, or Linux AppImage from the official Astera GitHub release, plus documentation links to the repository.

The main navigation and footer link to the Guide. Moving between the landing page and Guide keeps the selected theme and language. The design review has Home/Guide controls for checking both pages at the same viewport sizes. Smart Resume, How It Works, and Agent browser have no experimental badge; the Guide explains how to enable each feature.

The 2026-11-02 update checks Astera's v1.4.16 and v1.5.0 release notes, CLI definitions, Remote Runtime documentation, SDK, and Settings labels at local `main` HEAD `231e23f7`. It keeps the existing design and locale generator. Search/download checks, generated-page consistency, translation keys, IDs, anchors, Guide section order, command parity, and JavaScript syntax passed. The Astera browser loaded the Korean Guide and followed its new MCP & Skills contents link with no console errors. One font request reported `ERR_CACHE_MISS`; screenshot capture failed with a five-second paint timeout, so visual and responsive checks remain unverified. No app release, push, or deployment was performed. See the [dated source notes](docs/product-positioning.md).

The 2026-11-24 update checks Astera's v1.5.1 through v1.5.5 release notes, Jobs guide, CLI reference, usage guide, and English and Korean UI strings at local `develop` HEAD `1a8ec227`, which `origin/main` contains. It adds the External reviewers and Kubernetes Guide sections and corrects the earlier statement that Claude Code's shell is unrestricted on Windows. The new Korean copy was polished with the humanize-korean skill (structural gate passed at a 0.5% change rate), then checked against the English for matching links, code, and emphasis. Locale generation, search/download checks, translation keys, IDs, anchors, tag balance, JavaScript syntax, and whitespace passed. The Astera browser loaded both Guides and both home pages with no console errors; one font request reported `ERR_CACHE_MISS`. Screenshot attempts got no answer from the app within 15 seconds, so visual and responsive checks remain unverified. No push or deployment was performed. See the [dated source notes](docs/product-positioning.md).

The 2026-10-16 follow-up checks Astera v1.4.14 at `58c2893c`, matching the freshly fetched `origin/develop`. It adds finding limits/counts, event payload details, provider helpers and cancellation, notification catch-up/expiry, log limits, and the macOS manual-install action to both Guide languages. The [dated source notes](docs/product-positioning.md) distinguish these Guide updates from internal performance fixes.

The 2026-10-15 Guide update was checked against local Astera `develop` at `0cb5d195`, including the plugin, SDK, source picker, and completion-check changes planned for the next main release. At the user's direction, these are documented as regular features with main-branch reference links. The implementation references and verification results are in the [dated source notes](docs/product-positioning.md).

The 2026-10-12 feature update was checked against local Astera `develop` at `20965bed` (v1.4.11). It adds Remote Runtime, Creative Hub, media viewing, Run diffs, Host recovery, and agent workspace/feature introductions in both languages. It qualifies the older local Host scheduling advice: enabling Remote keeps that Host running for future Jobs and questions, while the Runtime machine must remain awake. See the [dated source and verification notes](docs/product-positioning.md) for the evidence and checks.

The 2026-10-03 MCP update was checked against local Astera `develop` at `ff9b3e78`: `docs/mcp.md`, MCP registration and access code, and the Settings UI. It also updates the How It Works explanation for Host-managed Jobs. See the [dated source and verification notes](docs/product-positioning.md) for its checks. The earlier 2026-09-30 CLI update was checked against `fd48e939`: **Settings → CLI**, Windows user PATH registration, Terminal/Chat sessions, Chat permissions, skill installation, Job questions, and Host replacement after an incompatible update. All 29 command examples matched the source's command and option definitions. Search/download checks, generated Korean pages, and 38 browser language checks passed. The 16 layout combinations checked (Home/Guide × English/Korean × dark/light × 1440/320px) had no page-wide overflow, broken images, or missing anchors; long Guide commands scroll inside their code blocks. Those checks did not launch agent sessions or Jobs.

The earlier product-emphasis update added dedicated Smart Resume, orchestration-skill, and Host guides, and moved Optional features into the Work with Astera group. Its 38 browser language checks and static reference/translation checks passed. At that stage, the full layout rerun stopped at a 30-second browser-helper timeout and final visual captures were unavailable. The dated CLI verification above records the current checks.

Initial Guide validation: 30 interaction checks passed; the landing page passed 22. Both pages were checked at 1440, 768, 390, and 320px in both themes. Saved images are from earlier landing-page iterations; a Guide capture was unavailable because the agent browser did not paint within its screenshot timeout.

Before localization, the expanded Guide passed all eight layout checks on 2026-09-22, with no overflow, missing images, or broken anchors. Background rendering limited some dynamic checks at that stage; see [design direction](docs/design-direction.md) for that history. The bilingual review above supersedes those results.

The [feature coverage review](docs/design-direction.md#기능-가이드-보강과-누락-검토--2026-09-22) maps the app's documented features to Guide sections. The How It Works walkthrough GIF and the existing Jobs GIF are included in the **Astera app README**, at `D:\parsingk\astera\README.md`.

The product screenshots are unchanged originals. Feature diagrams illustrate behavior; they are not screenshots. Download buttons read the latest GitHub release and link straight to the installer for the visitor’s OS. If the release cannot be checked or no matching file is available, they open the release page for manual selection. Linux defaults to the x86_64 AppImage. GitHub Pages serves the plain static files at `astera.run`.

See [design direction](docs/design-direction.md) for reference research, content boundaries, and review criteria.

The 2026-10-20 v1.4.15 update uses the app's release notes, README, and Jobs guide at local HEAD `ceda8763`. Search and download checks, locale generation, translation keys, anchors, Guide section order, command parity, JavaScript syntax, and whitespace checks passed. Astera's browser reported no console or network errors on all four changed pages in the final read-through. Screenshot capture timed out; the coordinator took ownership of screenshots before the local commit. No publishing or push was performed.

## Asset provenance

Images, the icon, and videos were copied from `D:\parsingk\astera`. The original `rolling-demo.gif`, `schedule-demo.gif`, and `jobs-demo.gif` are unchanged copies of the recordings embedded in the app README. Each matching `*-demo-still.png` is its unmodified first frame, extracted for reduced-motion display. Public Sans was copied from the app's bundled fonts, with its OFL license in `assets/fonts/PublicSans-LICENSE.txt`.

`assets/starfield.svg` is an original vector illustration of stars created for this website; the surrounding nebula is drawn with CSS gradients.

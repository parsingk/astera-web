# Astera website concept

Visual concept for Astera's promotional website, with light and deep navy themes, original product imagery, and English copy. Plain HTML, CSS, and JavaScript; no package installation or build step.

## Preview

From `D:\parsingk\astera-web`:

```powershell
python -m http.server 5173 --bind 127.0.0.1
```

Open http://127.0.0.1:5173. `index.html` can also be opened directly for a basic offline preview.

Direct previews: [dark](http://127.0.0.1:5173/?theme=dark) and [light](http://127.0.0.1:5173/?theme=light). The header and footer theme buttons update the URL, so the selected theme survives a reload and can be shared as a link. Without a theme parameter, the page and design review open in dark mode. Only `?theme=light` explicitly selects light mode.

[Design review](http://127.0.0.1:5173/design/review.html) offers 1440, 768, 390, and 320px viewports plus layout and interaction checks. This review page needs the HTTP server. Saved previews: [desktop](design/desktop.png) and [mobile](design/mobile-review.png).

The review page also has Light/Dark controls. [Open the dark review](http://127.0.0.1:5173/design/review.html?theme=dark). Dark captures: [desktop](design/dark-desktop.png), [mobile](design/dark-mobile-review.png), and [features](design/dark-features-review.png).

## Included

- Responsive landing page with real Astera screenshots and original icon.
- Terminal-first product preview with a Chat/Terminal switch and an enlarged screenshot dialog.
- Three existing product demo videos, opened with native playback controls.
- FAQ, mobile navigation, and synchronized header/footer theme controls.
- Local fonts and media, with no third-party runtime requests.
- Download and documentation links to the existing Astera GitHub repository.

The product screenshots are unchanged originals. Feature diagrams illustrate behavior; they are not screenshots. Download links open GitHub Releases rather than selecting an installer automatically. Public deployment and production framework selection remain outside this design pass.

See [design direction](docs/design-direction.md) for reference research, content boundaries, and review criteria.

## Asset provenance

Images, the icon, and videos were copied from `D:\parsingk\astera`. Public Sans was copied from the app's bundled fonts, with its OFL license in `assets/fonts/PublicSans-LICENSE.txt`.

# Contributing to Slidesmith

Thanks for your interest. Slidesmith is deliberately small and dependency-free — contributions should
keep it that way.

## Principles

- **No runtime dependencies.** The engine is Python standard library only. Please don't add pip
  packages; if something genuinely needs one, open an issue to discuss first.
- **Tokens are the source of truth.** Slides reference `var(--token)`; they must not hardcode hex
  values (the one allowed exception is ECharts series colors, which cannot read CSS variables — there,
  resolve from tokens by semantic role, as `engine/graphics_templates.py` does).
- **Offline and self-contained.** No network fetches at render time — no remote fonts, CDNs, or
  images. Bundled assets are loaded by local path only.
- **Two paths, one renderer.** Keep the basic (template) and advanced (agentic) paths converging on
  `engine/render.py`. See [`docs/ART-DIRECTION.md`](docs/ART-DIRECTION.md) for the authoring contract.

## Development setup

```bash
export CHROME_BIN=/path/to/chrome     # if not on the macOS default path
make css                              # compile tokens -> design/brand.css
make examples                         # render the reference gallery
```

You need Python 3.9+ and a Chrome/Chromium binary. There is nothing else to install.

## Making a change

1. Fork and branch.
2. If you change `design/tokens.json`, run `make css` and commit the regenerated `design/brand.css`.
3. If you change the engine or a bundled example, run `make examples` and eyeball
   `examples/expected/*.png` — every frame must be exactly the frame size (1080×1350 or 1080×1080)
   and stay on-brand.
4. Keep commits focused; describe *why*, not just *what*.

## Adding a new agentic layout example

1. Author `examples/slides/<name>.html` per `docs/ART-DIRECTION.md` (`/*@BRAND_CSS@*/` first in
   `<style>`, `var(--…)` throughout, Sora only, exact frame size).
2. Add a render line to the `examples` target in the `Makefile`.
3. Run `make examples` and include the generated PNG.

## Reporting issues

Please include: your OS, Python version, `CHROME_BIN` / Chrome version, the exact command, and the
full output. A minimal HTML slide that reproduces the problem helps a lot.

## Licensing of contributions

By contributing, you agree that your contributions are licensed under the project's [MIT](LICENSE)
license. Do not add third-party assets unless their license permits redistribution and you update
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

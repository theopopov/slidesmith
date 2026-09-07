# Third-Party Notices

Slidesmith bundles two third-party assets so that rendering works fully offline, with no CDN or
network access. Each is redistributed under its own license, reproduced in full alongside the asset.
These licenses are independent of the MIT license that covers Slidesmith's own source code.

---

## 1. Sora (typeface)

- **File:** `engine/assets/Sora.ttf` (also embedded as a base64 `@font-face` inside the compiled
  `design/brand.css`).
- **Copyright:** Copyright 2019 The Sora Project Authors (https://github.com/sora-xor/sora-font)
- **License:** SIL Open Font License, Version 1.1 — full text in `engine/assets/OFL.txt`.
- **Reserved Font Name:** "Sora". Per the OFL, if you create a modified version you must rename it;
  you may not use the Reserved Font Name for a derivative.
- The font is redistributed unmodified.

## 2. Apache ECharts (charting library)

- **File:** `engine/assets/echarts.min.js`
- **Version:** 5.6.1
- **Copyright:** © The Apache Software Foundation and contributors.
- **License:** Apache License, Version 2.0 — full text in `engine/assets/ECharts-LICENSE.txt`.
- The library is redistributed unmodified. It is loaded locally by `file://` path at render time
  (see `docs/ART-DIRECTION.md` and the `stat` template in `engine/graphics_templates.py`).

---

If you re-theme Slidesmith with a different typeface, replace `engine/assets/Sora.ttf`, update the
`@font-face`/`font.family.*` tokens in `design/tokens.json`, and update this file accordingly.

#!/usr/bin/env python3
"""render.py — rasterize a self-contained HTML file → 1080×1080 PNG via headless Chrome.

You author an on-brand HTML slide (inline CSS from design/tokens.json via the /*@BRAND_CSS@*/
marker, optional inline ECharts from engine/assets/echarts.min.js, the Sora font from
engine/assets/Sora.ttf), then this rasterizes it. Fully offline, no external service.

    python engine/render.py slide.html slide.png
    python engine/render.py slide.html slide.png --size 1080,1350

Set CHROME_BIN if Chrome isn't at the macOS default path.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = os.environ.get(
    "CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


BRAND_MARKER = "/*@BRAND_CSS@*/"


def render(html: str, out_png: str, *, size: str = "1080,1080", budget_ms: int = 5000,
           brand_css: str | None = None) -> str:
    """HTML string → PNG via headless Chrome.

    If `brand_css` (a path to design/brand.css) is given and the HTML contains the marker
    `/*@BRAND_CSS@*/`, the marker is replaced with the compiled tokens CSS before rendering. This
    lets agentic slides stay small (they write var(--…) + the marker) while still rendering on-brand,
    injecting the design system at render time.
    """
    if brand_css and BRAND_MARKER in html:
        html = html.replace(BRAND_MARKER, Path(brand_css).read_text(encoding="utf-8"))
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(html)
        html_path = fh.name
    try:
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=1", f"--window-size={size}",
               "--allow-file-access-from-files", "--no-sandbox",
               f"--virtual-time-budget={budget_ms}", f"--screenshot={out_png}",
               f"file://{html_path}"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if not Path(out_png).exists() or Path(out_png).stat().st_size == 0:
            raise RuntimeError(f"empty render (is Chrome at {CHROME}?): {r.stderr[-300:]}")
        return out_png
    finally:
        os.unlink(html_path)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Rasterize an HTML file → PNG (headless Chrome).")
    ap.add_argument("html", help="path to a self-contained .html file")
    ap.add_argument("out", help="output .png path")
    ap.add_argument("--size", default="1080,1080", help="WxH, e.g. 1080,1080 or 1080,1350")
    ap.add_argument("--brand-css", default=None,
                    help="path to design/brand.css; if the HTML has a /*@BRAND_CSS@*/ marker it is injected")
    a = ap.parse_args(argv)
    html = Path(a.html).read_text(encoding="utf-8")
    out = render(html, a.out, size=a.size, brand_css=a.brand_css)
    print(f"[render] {out} ({Path(out).stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

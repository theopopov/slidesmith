#!/usr/bin/env python3
"""graphics_templates.py — deterministic, on-brand slide builders (the basic path).

Each builder returns a self-contained HTML document that inlines design/brand.css (design tokens ->
CSS variables), so it renders on-brand with zero external state except the pinned local assets (Sora
is embedded in brand.css as base64; ECharts is referenced from engine/assets by absolute file://
path, which engine/render.py allows via --allow-file-access-from-files).

These cover the STABLE roles — cover, cta, stat, statement — where a fixed composition is correct
every time. The expressive "shape" layouts (progression, comparison, matrix, ...) are authored as
HTML per docs/ART-DIRECTION.md (the advanced path); this module is the deterministic half of the
hybrid renderer.

THEME-AGNOSTIC: everything on-slide resolves from design/brand.css via var(--…). ECharts series
colors (the one place canvas cannot read CSS vars) are resolved at build time from design/tokens.json
by SEMANTIC role name (accent / context / positive / negative / warning / ink / line), so charts are
automatically on-brand for any theme with the standard token schema. No per-theme edits to this
file.

    python engine/graphics_templates.py cover     copy.json out.html --size 1080,1350 --pager "01 / 04"
    python engine/graphics_templates.py statement copy.json out.html
    python engine/graphics_templates.py stat      copy.json out.html
    python engine/graphics_templates.py cta       copy.json out.html --pager "04 / 04"

copy.json is a small dict of the slide's text fields (see each builder's docstring).
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BRAND_CSS = (ROOT / "design" / "brand.css")
BRAND_JSON = (ROOT / "design" / "brand.json")
TOKENS_JSON = (ROOT / "design" / "tokens.json")
ECHARTS = f"file://{HERE / 'assets' / 'echarts.min.js'}"

# Semantic chart roles -> the token names that carry them (stable across themes: same token schema).
# Each maps to an ordered list of candidate token names; the first that resolves wins. Alias keys
# (signal/slate/amber/red/…) point at the same candidates so both the semantic vocabulary and common
# primitive-ish names resolve — a chart color never silently falls back to grey.
CHART_ROLE_TOKENS = {
    "accent":   ["color.bg.accent", "color.text.highlight"],
    "context":  ["color.text.muted", "color.slate.300", "color.slate.500"],
    "positive": ["color.status.up", "color.signal.500"],
    "negative": ["color.status.down", "color.red.500"],
    "warning":  ["color.amber.400", "color.status.down"],
    "ink":      ["color.text.default", "color.ink.900"],
    "line":     ["color.border.subtle", "color.line.200"],
}
# forgiving aliases → canonical role
CHART_ROLE_TOKENS.update({
    "primary": CHART_ROLE_TOKENS["accent"], "signal": CHART_ROLE_TOKENS["accent"],
    "emerald": CHART_ROLE_TOKENS["accent"],
    "muted": CHART_ROLE_TOKENS["context"], "slate": CHART_ROLE_TOKENS["context"],
    "gray": CHART_ROLE_TOKENS["context"], "grey": CHART_ROLE_TOKENS["context"],
    "up": CHART_ROLE_TOKENS["positive"], "green": CHART_ROLE_TOKENS["positive"],
    "down": CHART_ROLE_TOKENS["negative"], "red": CHART_ROLE_TOKENS["negative"],
    "amber": CHART_ROLE_TOKENS["warning"], "orange": CHART_ROLE_TOKENS["warning"],
    "border": CHART_ROLE_TOKENS["line"],
})
DEFAULT_CHART_CYCLE = ["context", "accent", "warning", "negative"]
_FALLBACK_HEX = "#888888"


def _load_tokens_flat() -> dict:
    """Flatten tokens.json to {name: raw_value} across all sets (later sets can reference earlier)."""
    if not TOKENS_JSON.exists():
        return {}
    tok = json.loads(TOKENS_JSON.read_text())
    flat: dict[str, str] = {}
    for setname in (tok.get("order") or list(tok.get("sets", {}).keys())):
        for name, _ttype, value in tok["sets"][setname]:
            flat[name] = value
    return flat


def _resolve_token(name: str, flat: dict, _seen=None) -> str | None:
    """Follow {ref} chains to a final literal (e.g. a hex color)."""
    _seen = _seen or set()
    if name in _seen or name not in flat:
        return None
    _seen.add(name)
    v = flat[name]
    if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        return _resolve_token(v[1:-1], flat, _seen)
    return v if isinstance(v, str) else None


def _chart_hex(spec: str, flat: dict) -> str:
    """spec is a literal hex (#…), a semantic role (accent/context/…), or a raw token name."""
    if isinstance(spec, str) and spec.startswith("#"):
        return spec
    if spec in CHART_ROLE_TOKENS:
        for cand in CHART_ROLE_TOKENS[spec]:
            hexv = _resolve_token(cand, flat)
            if hexv:
                return hexv
        return _FALLBACK_HEX
    hexv = _resolve_token(spec, flat)  # allow a raw token name like "color.signal.500"
    return hexv or _FALLBACK_HEX


def _brand() -> dict:
    if BRAND_JSON.exists():
        d = json.loads(BRAND_JSON.read_text())
        return {"handle": d.get("handle", ""), "tagline": d.get("tagline", "")}
    return {"handle": "", "tagline": ""}


def _css() -> str:
    if not BRAND_CSS.exists():
        raise SystemExit("[graphics_templates] design/brand.css missing — run "
                         "`python engine/tokens_to_css.py design/tokens.json design/brand.css` first.")
    return BRAND_CSS.read_text()


_BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
{css}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;font-family:var(--font-family-body)}}
.board{{width:{w}px;height:{h}px;position:relative;display:flex;flex-direction:column;
  padding:var(--spacing-64)}}
.kicker{{font-size:var(--font-size-kicker);font-weight:var(--font-weight-bold);
  letter-spacing:.08em;text-transform:uppercase}}
.footer{{position:absolute;left:var(--spacing-64);right:var(--spacing-64);bottom:var(--spacing-40);
  display:flex;justify-content:space-between;align-items:center;font-size:var(--font-size-caption);
  font-weight:var(--font-weight-medium)}}
.spacer{{flex:1}}
</style></head><body>{body}{script}</body></html>"""


def _doc(body: str, w: int, h: int, script: str = "") -> str:
    return _BASE.format(css=_css(), w=w, h=h, body=body, script=script)


def _footer(pager: str, on_dark: bool) -> str:
    b = _brand()
    c = "var(--color-text-on-dark)" if on_dark else "var(--color-text-muted)"
    mark = " · ".join(x for x in (b["handle"], b["tagline"]) if x)
    return (f'<div class="footer" style="color:{c}">'
            f'<span>{mark}</span><span>{pager}</span></div>')


def _kicker(eyebrow: str, color_css: str) -> str:
    """Render the kicker only if there's an eyebrow (theme-neutral: no baked default label)."""
    return f'<div class="kicker" style="color:{color_css}">{eyebrow}</div>' if eyebrow else ""


# ── builders ──────────────────────────────────────────────────────────────────────────────────

def cover(c: dict, pager: str, w: int, h: int) -> str:
    """copy: {eyebrow, title, subtitle}"""
    body = f'''<div class="board" style="background:linear-gradient(150deg,var(--color-bg-hero-start),var(--color-bg-hero-end));
        box-shadow:var(--elevation-hero) inset;color:var(--color-text-on-dark)">
      {_kicker(c.get("eyebrow",""), "var(--color-text-highlight)")}
      <div class="spacer"></div>
      <h1 style="font-family:var(--font-family-heading);font-weight:var(--font-weight-black);
        font-size:var(--font-size-display);line-height:.98;letter-spacing:-.02em;text-wrap:balance">{c["title"]}</h1>
      <p style="font-size:var(--font-size-lead);font-weight:var(--font-weight-regular);
        margin-top:var(--spacing-24);max-width:18ch;opacity:.92">{c.get("subtitle","")}</p>
      <div class="spacer"></div>
      <div class="kicker" style="letter-spacing:.24em;color:var(--color-text-on-dark);opacity:.7">SWIPE →</div>
      {_footer(pager, True)}
    </div>'''
    return _doc(body, w, h)


def statement(c: dict, pager: str, w: int, h: int) -> str:
    """copy: {eyebrow, title, body}"""
    body = f'''<div class="board" style="background:var(--color-bg-dark);color:var(--color-text-on-dark)">
      {_kicker(c.get("eyebrow",""), "var(--color-text-highlight)")}
      <div class="spacer"></div>
      <h1 style="font-family:var(--font-family-heading);font-weight:var(--font-weight-bold);
        font-size:var(--font-size-headline);line-height:1.05;letter-spacing:-.01em;text-wrap:balance">{c["title"]}</h1>
      <p style="font-size:var(--font-size-body);color:var(--color-text-on-dark);opacity:.8;
        margin-top:var(--spacing-24);max-width:26ch">{c.get("body","")}</p>
      <div class="spacer"></div>
      {_footer(pager, True)}
    </div>'''
    return _doc(body, w, h)


def stat(c: dict, pager: str, w: int, h: int) -> str:
    """copy: {eyebrow, figure, figure_label, caption, chart?:{categories,values,colors?}}.

    A REAL ECharts horizontal bar (not a hand-drawn div) carries the data. If no `chart` is given,
    the figure stands alone. Chart colors resolve from tokens.json by semantic role (accent/context/
    positive/negative/warning) — literal hex, because canvas cannot read CSS vars.
    """
    ch = c.get("chart")
    chart_div = script = ""
    if ch and ch.get("categories") and ch.get("values"):
        flat = _load_tokens_flat()
        cats, vals = ch["categories"], ch["values"]
        cols = ch.get("colors") or []
        data = []
        for i, v in enumerate(vals):
            role = cols[i] if i < len(cols) else DEFAULT_CHART_CYCLE[i % len(DEFAULT_CHART_CYCLE)]
            data.append({"value": v, "itemStyle": {"color": _chart_hex(role, flat), "borderRadius": 10}})
        ink = _chart_hex("ink", flat)
        chart_opt = {
            "grid": {"left": 0, "right": 0, "top": 6, "bottom": 0, "containLabel": False},
            "xAxis": {"type": "value", "max": max(vals) * 1.02, "show": False},
            "yAxis": {"type": "category", "data": cats, "show": False},
            "series": [{
                "type": "bar", "data": data, "barWidth": 46,
                "label": {"show": True, "position": "insideLeft", "distance": 18,
                          "formatter": "{b}", "color": ink, "fontFamily": "Sora",
                          "fontWeight": 600, "fontSize": 26},
            }],
            "animation": False,
        }
        chart_div = '<div id="chart" style="width:100%;height:170px;margin-top:var(--spacing-32)"></div>'
        script = (f'<script src="{ECHARTS}"></script>'
                  f'<script>echarts.init(document.getElementById("chart"))'
                  f'.setOption({json.dumps(chart_opt)});</script>')
    fig_label = c.get("figure_label", "")
    label_html = (f'<div style="font-size:var(--font-size-subhead);font-weight:var(--font-weight-semibold);'
                  f'color:var(--color-text-muted)">{fig_label}</div>') if fig_label else ""
    body = f'''<div class="board" style="background:var(--color-bg-surface);color:var(--color-text-default)">
      {_kicker(c.get("eyebrow",""), "var(--color-bg-accent)")}
      <div class="spacer"></div>
      <div style="display:flex;align-items:baseline;gap:var(--spacing-20)">
        <div style="font-family:var(--font-family-heading);font-weight:var(--font-weight-black);
          font-size:var(--font-size-hero);line-height:.9;letter-spacing:-.03em">{c["figure"]}</div>
        {label_html}
      </div>
      {chart_div}
      <p style="font-size:var(--font-size-body);color:var(--color-text-muted);
        margin-top:var(--spacing-24);max-width:28ch">{c.get("caption","")}</p>
      <div class="spacer"></div>
      {_footer(pager, False)}
    </div>'''
    return _doc(body, w, h, script=script)


def cta(c: dict, pager: str, w: int, h: int) -> str:
    """copy: {eyebrow, headline, action}"""
    body = f'''<div class="board" style="background:var(--color-bg-accent);color:var(--color-text-on-accent)">
      {_kicker(c.get("eyebrow",""), "var(--color-text-on-accent)")}
      <div class="spacer"></div>
      <h1 style="font-family:var(--font-family-heading);font-weight:var(--font-weight-black);
        font-size:var(--font-size-display);line-height:.98;letter-spacing:-.02em;text-wrap:balance">{c["headline"]}</h1>
      <div class="spacer"></div>
      <div style="display:inline-flex;align-self:flex-start;background:var(--color-action-onDark-bg);
        color:var(--color-action-onDark-text);font-weight:var(--font-weight-bold);
        font-size:var(--font-size-body);padding:var(--spacing-20) var(--spacing-40);
        border-radius:var(--radius-button)">{c.get("action","")}</div>
      {_footer(pager, True)}
    </div>'''
    return _doc(body, w, h)


BUILDERS = {"cover": cover, "stat": stat, "statement": statement, "cta": cta}
# role/layout aliases → builder
ALIASES = {"hero": "cover", "proportion": "stat", "definition": "statement"}


def build(role: str, copy: dict, out_html: Path, *, size: str = "1080,1350", pager: str = "") -> Path:
    name = role if role in BUILDERS else ALIASES.get(role, "")
    if name not in BUILDERS:
        raise SystemExit(f"[graphics_templates] no template for role/layout '{role}'. "
                         f"Template roles: {sorted(BUILDERS)} (+ aliases {sorted(ALIASES)}). "
                         f"Everything else is authored in-session per ART-DIRECTION.md.")
    w, h = (int(x) for x in size.split(","))
    html = BUILDERS[name](copy, pager, w, h)
    out_html.write_text(html, encoding="utf-8")
    return out_html


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build one on-brand slide (deterministic template) → HTML.")
    ap.add_argument("role", help="cover | statement | stat | cta (aliases: hero, proportion, definition)")
    ap.add_argument("copy", help="path to a JSON dict of the slide's text fields")
    ap.add_argument("out", help="output .html path")
    ap.add_argument("--size", default="1080,1350", help="WxH, e.g. 1080,1350 (4:5, default) or 1080,1080 (1:1)")
    ap.add_argument("--pager", default="", help="carousel pager, e.g. '01 / 04' (blank for single graphics)")
    a = ap.parse_args(argv)
    copy = json.loads(Path(a.copy).read_text())
    out = build(a.role, copy, Path(a.out), size=a.size, pager=a.pager)
    print(f"[graphics_templates] wrote {out} (role={a.role}, size={a.size})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

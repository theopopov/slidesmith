#!/usr/bin/env python3
"""tokens_to_css.py — compile design/tokens.json → design/brand.css (CSS custom properties).

The design system stays the single source of truth: tokens.json is compiled here into
`:root { --… }` variables + a Sora @font-face, so every graphic is on-brand by construction.
Token references ({color.signal.500}) become var(--color-signal-500), so the semantic layer
resolves at CSS runtime exactly as it does in Penpot — one brand source, no template fork.

SELF-CONTAINED FONT: `engine/render.py` writes the slide HTML to a temp file in the system temp
dir, so a relative `url('assets/Sora.ttf')` would NOT resolve. We therefore embed Sora as a base64
`data:` URI, so brand.css is fully self-contained and every rendered slide carries the font with
zero external state.

    python engine/tokens_to_css.py design/tokens.json design/brand.css
    python engine/tokens_to_css.py design/tokens.json design/brand.css --font-file engine/assets/Sora.ttf
"""
from __future__ import annotations
import argparse, base64, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_FONT = HERE / "assets" / "Sora.ttf"

PX_TYPES = {"spacing", "borderRadius", "borderWidth", "fontSizes", "dimension", "sizing"}


def var_name(token_name: str) -> str:
    return "--" + token_name.replace(".", "-").replace("/", "-")


def _ref(v: str) -> str | None:
    v = v.strip()
    if v.startswith("{") and v.endswith("}"):
        return f"var({var_name(v[1:-1])})"
    return None


def value_to_css(ttype: str, value) -> str:
    # reference to another token → var()
    if isinstance(value, str) and (r := _ref(value)):
        return r
    if ttype == "fontFamilies":
        fams = value if isinstance(value, list) else [value]
        out = []
        for f in fams:
            out.append(_ref(f) if isinstance(f, str) and _ref(f) else f'"{f}"')
        return ", ".join(out) + ", system-ui, sans-serif"
    if ttype in PX_TYPES:
        return f"{value}px"
    if ttype == "fontWeights":
        return str(value)
    if ttype == "shadow":
        parts = value if isinstance(value, list) else [value]
        segs = []
        for s in parts:
            inset = "inset " if s.get("inset") else ""
            segs.append(f'{inset}{s["offsetX"]}px {s["offsetY"]}px {s["blur"]}px {s.get("spread",0)}px {s["color"]}')
        return ", ".join(segs)
    return str(value)  # color + fallback


def _font_face(font_file: Path) -> str:
    """Sora @font-face with the TTF embedded as a base64 data: URI (self-contained)."""
    if not font_file.exists():
        raise SystemExit(f"[tokens_to_css] font not found: {font_file}")
    b64 = base64.b64encode(font_file.read_bytes()).decode("ascii")
    return ("@font-face { font-family:'Sora'; font-style:normal; font-weight:100 800;\n"
            f"  src:url(data:font/ttf;base64,{b64}) format('truetype'); font-display:block; }}")


def compile_css(tokens: dict, font_file: Path) -> str:
    lines = [
        "/* AUTO-GENERATED from design/tokens.json by engine/tokens_to_css.py — do not edit.",
        "   One brand source of truth. Regenerate after changing tokens.json. */",
        _font_face(font_file),
        ":root {",
    ]
    # primitives first (definitions), then modes/light, then semantic (references resolve via var)
    order = tokens.get("order") or list(tokens.get("sets", {}).keys())
    for setname in order:
        lines.append(f"  /* set: {setname} */")
        for name, ttype, value in tokens["sets"][setname]:
            lines.append(f"  {var_name(name)}: {value_to_css(ttype, value)};")
    # shadow primitives (kept separate in tokens.json)
    for name, val in (tokens.get("shadow_primitives") or {}).items():
        if name.startswith("_"):
            continue
        lines.append(f"  {var_name(name)}: {value_to_css('shadow', val)};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Compile design tokens.json → brand.css (CSS custom properties).")
    ap.add_argument("tokens")
    ap.add_argument("out")
    ap.add_argument("--font-file", default=str(DEFAULT_FONT),
                    help="TTF to embed as the Sora @font-face (default: engine/assets/Sora.ttf)")
    a = ap.parse_args(argv)
    tokens = json.loads(Path(a.tokens).read_text())
    css = compile_css(tokens, Path(a.font_file))
    Path(a.out).write_text(css, encoding="utf-8")
    nvars = css.count("\n  --")
    print(f"[tokens_to_css] wrote {a.out} ({nvars} vars, font embedded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# ART-DIRECTION — the agentic authoring CONTRACT (the advanced path)

This is the single biggest graphics-quality lever. When the pipeline routes a slide to the
**agentic** path (any layout not marked `template` in `LAYOUT-TAXONOMY.md`), **the complete HTML is
authored under this contract** — by you, or by any capable designer/agent. There is no LLM
subprocess in this repo; the author *is* the designer. This document is the brief they follow.

Author one slide at a time. Follow the brief for that slide (its `role`, `layout_id`,
`copy_char_budget`, and fitted copy — produced by the PLAN and COPY-FIT steps; see
`.claude/commands/graphics.md`).

---

## ROLE — Senior social-graphics designer (HTML author)
You design a single, production-grade social graphic and return it as ONE complete, self-contained
HTML document. You are judged on visual design: hierarchy, an intentional composition specific to
THIS beat, professional typography, spacing, and a single clear focal point. Ship a graphic a studio
would send a client.

## Output contract (STRICT)
- Save ONE HTML document per slide — starts at `<!doctype html>`, ends at `</html>`. Real content
  from the brief — never lorem, never placeholder.
- The page MUST be exactly the frame's pixel size (e.g. `1080×1350` for 4:5, or `1080×1080` for
  1:1): `html,body{margin:0;padding:0;width:<W>px;height:<H>px;overflow:hidden}` and a single root
  container of the same size. Keep meaningful content off the outer ~64px margin.
- Inline ALL your CSS in a `<style>`, whose first line is the `/*@BRAND_CSS@*/` marker (see BRAND).

## BRAND — non-negotiable (the render mechanism)
- **Put the marker `/*@BRAND_CSS@*/` as the very first line inside your `<style>`.** At render time,
  `engine/render.py --brand-css design/brand.css` replaces it with the compiled tokens CSS (every
  design token as a CSS custom property, plus the embedded Sora font). This keeps your slide file
  small while it still renders fully on-brand. (Do NOT paste the large brand.css by hand, and do NOT
  `@import` it — the marker is the mechanism.)
- **Reference tokens via `var(--…)`** for every fill, text color, type size, radius, spacing, and
  shadow. Do NOT hardcode hex values — a raw `#12B981` is a defect; use `var(--color-signal-500)`.
  (The ONLY exception: ECharts series colors, which render to `<canvas>` and cannot read CSS vars —
  there, use the literal brand hex.)
- **Sora only.** Do NOT `@import` Google Fonts or any remote font. Sora is already embedded in
  brand.css; the renderer runs offline.
- Follow `design/DESIGN.md`: deep terminal-ink grounds, ONE emerald `signal.500` accent, generous
  whitespace, Sora set tight. `amber.400` is allowed ONLY for a caution fact (a warning, a flag) —
  the single exception to the one-accent rule.
- Fixed footer band: brand mark left (from `design/brand.json`, caption/16, muted), pager right
  (`NN / NN`) on carousel slides. Kicker (uppercase, kicker/22) top-left as the category label.

## Techniques you MAY use (all render headless in Chrome)
- CSS: gradients (linear/radial/conic), grid & flex, transforms, filters, blend-modes, clip-path,
  shadows. Use flex/grid for stacks and rows — never hand-place with magic numbers when a layout fits.
- Illustration / marks: inline `<svg>` (icons, arrows, diagram nodes, terminal chrome).
- Generative background: a full-bleed `<canvas>` with SEEDED randomness (deterministic — no
  `Math.random()` without a fixed seed). Encouraged for texture, used sparingly.
- Charts / data-viz: if the beat has series data, include a REAL chart with ECharts, loaded from
  EXACTLY this local path: `<script src="file://<ABSOLUTE_PATH>/engine/assets/echarts.min.js"></script>`
  then `echarts.init(el).setOption({…})`. Style series to the brand hex. Prefer a real chart over
  faking bars with divs. (For simple stat/proportion beats, the `stat` template already does this —
  agentic charts are for richer shapes: trend history, adoption curves, cost-over-time.) Compute the
  absolute ECharts path once:
  `python3 -c "import pathlib;print('file://'+str(pathlib.Path('engine/assets/echarts.min.js').resolve()))"`.

## Forbidden
- No external raster images (`<img src="http…">`), no remote scripts except the local ECharts path,
  no network fetches (no remote fonts, no CDNs). No placeholder text.
- No em dashes (—) in on-graphic copy — recast to a period, colon, comma, or parentheses.
- No hype register. (If your project keeps a forbidden-terminology list, enforce it at authoring
  time; Slidesmith ships no list of its own and no code reads one.) No invented numbers — every
  figure must trace to your source copy.

## Quality bar
Distinctive, on-theme art direction — a different, considered look per beat, not a template reskin.
ONE focal point; ONE emphasis move (a single word or number in `text.highlight` emerald). One idea
per slide, sayable in a sentence; ≤30 words total; headline ≤8 words. If numbers are given,
visualize them. When done, hand the file to the RENDER step:
`python engine/render.py <slide>.html <slide>.png --size <W,H> --brand-css design/brand.css`.

---

## Authoring loop (per agentic slide)
1. Read the slide's brief (`role`, `layout_id`, `copy_char_budget`, `source`) and its fitted copy.
2. Pick the composition that matches the `layout_id` (see `LAYOUT-TAXONOMY.md` copy_function) — e.g.
   `comparison` → two panels; `progression` → staged value→value rows; `useful_drop` → name-hero card
   with class + activity chips; `stack_diagram` → horizontal tile flow with signal arrows.
3. Author the HTML per the contract above: `/*@BRAND_CSS@*/` first in `<style>`, `var(--…)` throughout.
4. Save the `.html` and render:
   `python engine/render.py <slide>.html <slide>.png --size <W,H> --brand-css design/brand.css`.

_See `examples/slides/` for worked, renderable examples of the advanced path across the layout
vocabulary._

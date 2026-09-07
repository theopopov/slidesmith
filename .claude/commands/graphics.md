Author + render on-brand slide graphics — as a senior designer, in five gated steps.

This is the optional agent driver for Slidesmith. It runs the graphics pipeline (plan → slide-copy →
author → render → review) one step at a time. Do NOT one-shot HTML from a blank canvas. Work one
step at a time and show the result before advancing. Everything is offline (no keys, no services).

Read first (once): `design/DESIGN.md`, `design/graphics-format-library.json`,
`docs/{LAYOUT-TAXONOMY.md, SLIDE-COUNT-RUBRIC.md, ART-DIRECTION.md}`,
`design/slide-layout-library.json`. Source copy is whatever post text you are turning into a deck.

---

## RULE · Per-deck output folder
**Every deck gets its OWN output folder under `out/`.** Before authoring anything (Step A), create
`out/<deck>/` and save ALL of this deck's artifacts there: `plan.json`, `slide_copy.md`, every
`*.html`, every `*.png`. `out/` is gitignored scratch; committed examples live in `examples/`.

---

## Step A · PLAN (structure before pixels)
1. Ensure the brand stylesheet is current: if `design/brand.css` is missing or older than
   `design/tokens.json`, run `python engine/tokens_to_css.py design/tokens.json design/brand.css`.
2. Pick the **frame** from `design/graphics-format-library.json` by post type (default
   `carousel_narrative`, 4:5 → 1080×1350; use `carousel_comparison` for contrast/myth-bust,
   `carousel_listicle` for graded lists, `single` 1:1 for a standalone graphic).
3. Apply `SLIDE-COUNT-RUBRIC.md`: from the source copy, build the ordered core-message units
   (proof > insight > implication) and decide the message-slide count; clamp to the frame's
   min/max. Cover + cta are fixed.
4. For each slide assign `{role, layout_id (via LAYOUT-TAXONOMY.md, constrained to the frame's
   allowed_layouts), copy_char_budget (from the layout/role), source (which line of the copy)}`.
5. Write `out/<deck>/plan.json`:
   `{frame, aspect_ratio, size, slide_count_decision:{count, rubric_trace:[…]}, slides:[{index, role,
   layout_id, layout_rationale, copy_char_budget, render:"template|agentic", source}]}`.
6. Show the plan as a short wireframe (slide N · role · layout · one-line why). **Wait for
   approval** before authoring anything.

## Step B · COPY-FIT (fit micro-copy to each slide's budget)
For each slide, distill the source line(s) into the layout's `copy_function`, within
`copy_char_budget` (aim comfortably under, not exactly at it). Preserve every number, name, date, and
category exactly. **No em dashes**; one emphasis word per slide. Write `out/<deck>/slide_copy.md`
(per slide: role, layout, `char_count <= budget`, the fitted text fields). Show it; wait for go.

## Step C · AUTHOR (the hybrid router)
For each slide, route by its `render` field (from the taxonomy):
- **template** (`cover`, `cta`, `stat`/`proportion`, `statement`/`definition`): write the slide's
  copy fields to a small JSON and build deterministically —
  `python engine/graphics_templates.py <role> <copy.json> out/<deck>/slide_<N>.html --size <W,H> --pager "NN / NN"`.
  (Stat copy may include a `chart:{categories,values,colors}` for a real ECharts bar.)
- **agentic** (everything else — `useful_drop`, `stack_diagram`, `comparison`, `progression`,
  `matrix`, `myth_reframe`, `problem_solution`, `quote`, `list`): **author the complete HTML
  in-session under `docs/ART-DIRECTION.md`** — put `/*@BRAND_CSS@*/` first in `<style>`, reference
  tokens via `var(--…)`, Sora only, one focal point, one emphasis move. Save to
  `out/<deck>/slide_<N>.html`.

## Step D · RENDER
Rasterize each slide at the frame size. Template slides are self-contained; agentic slides need the
brand-css injection (the `--brand-css` flag is harmless for template slides, so pass it every time):
`python engine/render.py out/<deck>/slide_<N>.html out/<deck>/slide_<N>.png --size <W,H> --brand-css design/brand.css`

## Step E · REVIEW
Show the PNG paths in posting order. Iterate on feedback — a fix is usually a copy-fit tweak (step B)
or a re-author of one agentic slide (step C), not a full redo.

---

Notes:
- One idea per slide; the cover carries the hook, the cta the single soft ask. Keep the footer brand
  (from `design/brand.json`) + pager consistent across the carousel.
- Never invent a number — every figure on-graphic traces to your source copy. Represent categories
  accurately.

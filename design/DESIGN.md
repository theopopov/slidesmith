---
# Slidesmith default theme — graphics design system. Source of truth for the graphics pipeline, which
# runs a structured PLAN -> COPY-FIT -> AUTHOR -> RENDER -> REVIEW flow (see .claude/commands/graphics.md
# and docs/). Tokens compile to design/brand.css (via engine/tokens_to_css.py); slides reference
# var(--...). AUTHOR is HYBRID: stable roles (cover/cta/stat/statement) render deterministically via
# engine/graphics_templates.py; expressive layouts are authored per docs/ART-DIRECTION.md (the advanced
# path). Canvas is 4:5 (1080x1350) by default, 1:1 (1080x1080) for single graphics.
theme: Slidesmith default — a builder / developer-tool aesthetic. Voice-neutral; retheme via design/tokens.json.
canvas: { default: "4:5", sizes: { "4:5": [1080, 1350], "1:1": [1080, 1080] }, unit: px, grid: 4 }  # 4:5 default; 1:1 for single graphics
fonts: { family: Sora, weights: [400, 500, 600, 700, 800] }
colors:
  paper.100: "#FBFBF9"   # surface
  paper.200: "#F0F2ED"   # page bg
  ink.900: "#0F1419"     # text / dark bg (deep terminal ink)
  ink.700: "#1C242E"     # hero gradient end
  slate.500: "#5B6673"   # muted text
  signal.500: "#12B981"  # PRIMARY accent — the emerald signal
  signal.700: "#0B7D57"  # accent deep
  build.500: "#2F6FEB"   # secondary — build/link blue
  amber.400: "#F5A524"   # caution highlight (flags, warnings)
  line.200: "#DCE0D8"    # subtle border
  red.500: "#E5484D"     # status down / negative
  white: "#FFFFFF"
semantic:
  bg: { page: paper.200, surface: paper.100, dark: ink.900, accent: signal.500, hero: [ink.900→ink.700] }
  text: { default: ink.900, muted: slate.500, on-dark: paper.100, on-accent: ink.900, highlight: signal.500 }
  action: { primary: {bg: signal.500, text: ink.900}, accent: {bg: build.500, text: paper.100}, onDark: {bg: signal.500, text: ink.900} }
  border: { subtle: line.200, width: 1 }
  status: { up: signal.500, down: red.500 }
type_scale:  # px
  hero: 168    # single-word / short cover statements
  display: 120
  headline: 68
  subhead: 40
  lead: 34     # cover subtitle / body lead
  body: 28
  kicker: 22   # uppercase eyebrow / category label
  caption: 16  # footer brand + pager
radius: { sm: 6, md: 12, lg: 20, xl: 28, pill: 999, card: 20, button: 999, input: 12, badge: 6, tile: 12 }
spacing: { grid: 4, scale: [4,8,12,16,20,24,32,40,48,64,80], inset: {xs:8, sm:16, md:24, lg:40, xl:64}, gap: {sm:12, md:20, lg:32} }
shadow:
  card: "0 6 20 0 #0F14191A"        # elevation.card
  hero-glow: "0 0 120 12 #12B98159" # elevation.hero (emerald signal glow)
---

# Slidesmith default theme — design guide (for the agentic designer)

## Overview
A **builder / developer-tool** aesthetic: clean, technical, high-contrast, confident. Think a
well-designed dev-tool landing page or a sharp technical README. Deep terminal-ink grounds, a single
emerald "signal" accent, generous whitespace, and Sora set tight. Feels **credible, current, and
un-hyped**. Every graphic is 4:5 (1080×1350) by default — 1:1 (1080×1080) for a single standalone
graphic — and must read as one clear message. This is the *default* theme: swap `design/tokens.json`
to re-skin every slide without touching code.

## The graphics pipeline (how these rules get applied)
This guide is the *aesthetic* layer. The *procedure* lives in `.claude/commands/graphics.md` and the
three specs, which decide structure before pixels:
- `docs/SLIDE-COUNT-RUBRIC.md` — how many message slides (proof>insight>implication) + a
  post-type → slide-sequence map.
- `docs/LAYOUT-TAXONOMY.md` (+ `design/slide-layout-library.json`) — which layout each message beat
  becomes (a drop → `useful_drop`, a pipeline → `stack_diagram`, a contrast → `comparison`, …),
  with per-layout copy budgets.
- `docs/ART-DIRECTION.md` — the senior-designer authoring contract for bespoke slides.
- `design/graphics-format-library.json` — the frames (aspect, roles, allowed layouts).
Tokens compile to `design/brand.css` via `engine/tokens_to_css.py`; **reference `var(--…)`, never
raw hex** (the one exception is ECharts series colors, which use literal brand hex).

## Layout system
- Safe margin: keep meaningful content off the outer `spacing.inset.xl (64px)` on all sides.
- Fixed footer band (`spacing.inset.lg` from bottom): brand mark left (from `design/brand.json`,
  caption/16, muted), pager right = `NN / NN` (only on carousel slides).
- Kicker (uppercase, kicker/22, signal or muted) top-left as the category / capability label.
- One hero element per frame; one emphasis move max (a single word/number in `text.highlight`
  emerald). Caution facts (a warning, a flag) may use `amber.400` — that is the ONE exception to the
  single-accent rule, and only for a warning.
- Use flex/grid layout for stacks and rows; never hand-place with magic numbers when a layout fits.
- Apply TOKENS, never raw values (fills, type, radius, spacing, shadow all resolve from tokens).

## Roles → tokens
- **Cover / hero**: `bg.hero` (ink→ink gradient) or `bg.dark`; title in hero/display Sora 800
  `text.on-dark`; subtitle lead/34; `elevation.hero` emerald glow. Swipe cue bottom-left.
- **Useful drop** (product/release card): a `bg.surface` card — the name headline/68 Sora 700, a
  one-line "what it is", a chip row for a **class/category** chip and an **activity/metric** chip,
  and "where it fits". The name is the hero.
- **Statement / take**: `bg.surface`; headline/68 Sora 700 `text.default`; ≤1 emerald highlight word.
- **Stat / chart**: one dominant figure display/120–hero/168; caption lead/34 `text.muted`;
  ECharts for trend / adoption / comparison, drawn with token colors (signal for the hero series,
  slate for context, red for decline).
- **Stack diagram**: a horizontal `stage → stage → stage` flow of token-styled tiles with signal
  arrows; the "composes-with" story is the visual.
- **CTA**: `bg.dark` or `bg.accent`; directive headline; pill button `action.primary` (signal) or
  `action.accent` (build-blue). One ask only.

## Compositional systems (layout_id → on-brand look)
The two signature roles above (**useful_drop**, **stack_diagram**) plus these agentic layouts. Each
is ONE focal point, ONE emphasis move, tokens only. Render path per `slide-layout-library.json`.
- **comparison**: two equal panels split down the middle (or a diptych); a tag + one line each; the
  axis of contrast identical on both sides; the winning side gets the emerald word.
- **progression**: 3–5 stacked rows, `stage → value`, value climbing/falling; the final value is the
  emphasis; optional thin connective rule between rows.
- **matrix**: a 2×2 grid on `bg.surface` with `line.200` dividers; axis labels outside; four short
  quadrant labels; the target quadrant filled `signal.500`.
- **myth_reframe**: a struck / muted "myth" row on top, a solid `signal` "reality" row below; reality
  carries the emphasis.
- **problem_solution**: problem block in muted/ink, solution block in emerald; a downward arrow mark.
- **steps / list**: a kicker label + numbered (steps) or dotted (list) items, ≤5, tight leading; one
  item may carry the emphasis.
- **quote**: an oversized decorative glyph optional; quote in headline/68; attribution in body/28 muted.
- **definition**: term as the hero headline; a 1–2 line explanation below in muted body.
- **stat / proportion**: the number is the hero (display/120–hero/168); real ECharts only when there
  is series data. Rendered by the `stat` template.

## Word discipline (no character overload)
- One frame = one idea, sayable in a sentence. ≤30 words total per frame; headline ≤8 words.
- Charts/stats: the number is the hero — minimal surrounding words.
- A "useful drop" names the EXACT thing and its class — specificity is the substance.
- Never overload a slide; if it needs more, it is another slide (carousel).

## Do / Don't
- DO name exact things, numbers, categories — specificity is credibility.
- DO keep the footer brand + pager consistent across a carousel.
- DON'T use hype register or "game-changer" energy in on-graphic copy.
- DON'T use em dashes in on-graphic copy; DON'T invent numbers.
- DON'T restyle the palette or fonts inside a slide; retheme via `design/tokens.json` instead.

## Known gaps
- Typeface is Sora (the shipped render-engine @font-face). If a mono face is later added for
  code/CLI snippets, wire it as `font.family.mono` + a new @font-face asset; until then mono maps
  to Sora.

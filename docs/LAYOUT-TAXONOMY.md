# Slide-layout taxonomy — text → graphic classification

Consumed by the graphics **PLAN step** to pick, per message slide, which visual layout best fits
that beat's **text shape**. Topic-agnostic: it classifies the *structure* of the copy (a list, a
progression, a contrast, a product drop…), never the subject matter, and never pixels. The
machine-readable vocabulary is `design/slide-layout-library.json`; this doc is the human rationale.

## Why this exists
The slide-count rubric (`SLIDE-COUNT-RUBRIC.md`) decides *how many* message slides. This taxonomy
decides *what each one looks like*. Without it, message slides are invented blind to content and
drift in quality. Instead: a months-by-months figure becomes a **progression**, an author line
becomes a **quote**, "X vs Y" becomes a **comparison**, a just-shipped release becomes a
**useful_drop**.

## How selection works (the PLAN step applies this)
1. For each message beat (from the post copy), read its **text shape**.
2. Match the shape against each layout's `trigger_signals`; pick the **highest-priority** match.
3. **Constrain to the frame**: the chosen frame in `design/graphics-format-library.json` declares
   `allowed_layouts`. If the best match isn't allowed, fall back to the next allowed match, and
   ultimately to `statement`.
4. Record the chosen `layout_id` (and a one-line rationale) on the slide in the plan.

Nothing here is pixel-derived: `trigger_signals`, `copy_function`, and `copy_char_budget` are all
authored in `slide-layout-library.json`.

## Priority (specific beats beat generic)
`useful_drop > stack_diagram > progression > steps > comparison > matrix > myth_reframe >
problem_solution > definition > proportion > stat > quote > list > statement`
`statement` always matches last as the catch-all — any beat can render as a statement.

## The vocabulary

| layout_id | Fires when the beat's text is… | Copy shape | Budget | Render |
|---|---|---|---|---|
| **useful_drop** ★ | a specific just-shipped release / tool / product the audience can use today | name (hero) + what-it-is + class chip + activity chip + fits-in | 200 | agentic |
| **stack_diagram** ★ | a pipeline / composition of steps (stage→stage→…) | 3–6 tile labels joined by signal arrows | 140 | agentic |
| **progression** | the same metric across ordered stages/time; before→after numeric | staged rows value→value | 190 | agentic |
| **steps** | an ordered / numbered sequence or process (1→N) | label + numbered items | 200 | agentic |
| **comparison** | two contrasted sides (X vs Y, "not X but Y") | two panels, tag + line each | 200 | agentic |
| **matrix** | two crossed dimensions → four cells (2×2 trade-off) | axis names + four quadrant labels | 170 | agentic |
| **myth_reframe** | a wrong belief / common approach stated then corrected | myth row → reality row | 180 | agentic |
| **problem_solution** | an explicit pain → fix movement | problem block → solution block | 190 | agentic |
| **definition** | a concept is named and explained ("The dead zone is…") | term + explanation | 170 | template (statement) |
| **proportion** | a ratio / share ("N in M", "X%") | figure + proportion caption | 120 | template (stat) |
| **stat** | a single dominant number/metric | big figure + caption (+ real ECharts) | 120 | template (stat) |
| **quote** | an attributed line / testimonial | quotation + attribution | 180 | agentic |
| **list** | 3+ parallel, unordered points | label + ≤5 bullet items | 200 | agentic |
| **statement** | a single assertion with no internal structure (fallback) | headline + 1–3 lines | 160 | template (statement) |

★ = signature layouts (product-drop card + composes-with pipeline flow).

Plus the two fixed **roles** (structural position, not selected by trigger): **cover** (hero) and
**cta** — both template-rendered (`engine/graphics_templates.py`).

## Render path (the hybrid router)
- **template** → `engine/graphics_templates.py` builds it deterministically (pixel-consistent):
  `cover`, `cta`, `stat` (+ `proportion`), `statement` (+ `definition`).
- **agentic** → the complete HTML is authored per `docs/ART-DIRECTION.md`, brand-locked to
  `design/brand.css`. Everything else.

## Auditability
The PLAN step records the chosen `layout_id` + `layout_rationale` per slide in the plan, so a
reviewer can see *why* slide 3 became a `progression` and slide 5 a `useful_drop` before any HTML is
authored.

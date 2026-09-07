# Message-slide count rubric

Consumed by the graphics **PLAN step** to decide how many `message` slides a carousel needs. The
`cover` (first) and `cta` (last) slides are ALWAYS present and fixed — this rubric governs the
`message` slides *between* them only. Topic-agnostic: it reasons about narrative coverage, never
about subject matter, and never about pixels.

## Inputs (authored text only)
- The post copy, segmented into the distinct ideas it makes.
- Its **core-message units**: the beats that carry proof / insight / implication (the hook and the
  CTA line do NOT become message slides — the cover carries the hook, the cta slide the ask).
- The chosen frame's `min_slides` / `max_slides` and the platform carousel max (commonly 10).

## Principle
A carousel carries exactly as many `message` slides as it takes to represent the post body's
**core message once** — no filler, no dropped ideas. One message slide advances one self-contained
unit of that core message.

## Procedure (slide by slide)
1. Build the ordered set of **core-message units** from the post copy (merge a beat and a sentence
   that say the same thing into one unit — avoid duplicate slides).
2. `remaining` = that full set.
3. While `remaining` is non-empty:
   - Take the next-highest-priority uncovered unit. Priority: **proof > insight > implication**;
     ties break by the order they appear in the post.
   - Allocate one message slide for it; classify its layout via `LAYOUT-TAXONOMY.md`.
   - Remove it (and anything it subsumes) from `remaining`.
4. **Stop** as soon as `remaining` is empty. Do not add slides to round out a number.

## Bounds and clamping
- `count` = 1 (cover) + N (message) + 1 (cta).
- Clamp: `min_slides <= count <= min(frame.max_slides, 10)`.
- **Under min:** split the largest covered unit into its sub-points across extra message slides
  until `count == min_slides`. Never drop the cover or cta to hit a minimum.
- **Over cap:** keep the highest-priority units up to the cap; fold lower-priority points into the
  slides you keep.

## Post-type → slide-sequence map (starting shape; the rubric above still governs the count)
These are the *default spines*; the PLAN step adjusts the message count to the actual copy.

| Post type | Default spine (cover · message… · cta) | Typical count |
|---|---|---|
| **useful-drop teardown** (signature) | cover · **useful_drop** · stat\|list · stack_diagram\|comparison · cta | 4–5 |
| **composes-with** | cover · **stack_diagram** · useful_drop\|list · statement · cta | 4–5 |
| **build-vs-buy** | cover · comparison · comparison · matrix\|statement · cta | 5 |
| **alternative-to-X** | cover · useful_drop · comparison · stat · cta | 5 |
| **myth-bust** | cover · myth_reframe · definition\|statement · list · cta | 4–5 |
| **graded-list** | cover · list\|steps · stat\|proportion · cta | 3–4 |
| **opinion / take** | cover · statement · problem_solution\|progression · cta | 3–4 |
| **data flagship** | cover · stat (chart) · progression · list · statement · cta | 5–6 |

Single-graphic posts (not a carousel) use the `single` frame: one slide, role picked from the beat
(useful_drop / stat / statement), no pager.

## Auditability
Record the full decision — every message slide, which unit it covers, its layout, and whether core
message remained after it — in the plan under `slide_count_decision`. Show a reviewer this plan for
approval **before** authoring any HTML.

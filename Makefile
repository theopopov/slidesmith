# Slidesmith — build the brand stylesheet, render the demo carousel, regenerate examples.
# No dependencies to install. Requires Python 3.9+ and a Chrome/Chromium binary
# (set CHROME_BIN if it is not at the macOS default path — see .env.example).

PY      ?= python3
SIZE    := 1080,1350
BRAND   := design/brand.css
TOKENS  := design/tokens.json
DEMO    := out/demo
GALLERY := out/gallery

.PHONY: help css demo examples clean

help:
	@echo "Slidesmith targets:"
	@echo "  make css       Compile design/tokens.json -> design/brand.css"
	@echo "  make demo      Render the 6-slide demo carousel into $(DEMO)/"
	@echo "  make examples  Re-render the committed reference PNGs into examples/expected/"
	@echo "  make clean     Remove out/"
	@echo ""
	@echo "  Set CHROME_BIN if Chrome is not at the macOS default (see .env.example)."

# 1) Compile the design tokens into the brand stylesheet (one brand source of truth).
css:
	$(PY) engine/tokens_to_css.py $(TOKENS) $(BRAND)

# 2) The demo: a coherent 6-slide carousel. Slides 1/5/6 use the BASIC (template) path;
#    slides 2/3/4 use the ADVANCED (agentic) path (pre-authored HTML + brand-css injection).
demo: css
	@mkdir -p $(DEMO)
	# --- template path (basic): build HTML deterministically, then rasterize ---
	$(PY) engine/graphics_templates.py cover examples/copy/cover.json $(DEMO)/slide_1.html --size $(SIZE) --pager "01 / 06"
	$(PY) engine/render.py $(DEMO)/slide_1.html $(DEMO)/slide_1.png --size $(SIZE) --brand-css $(BRAND)
	# --- agentic path (advanced): render authored HTML with brand-css injection ---
	$(PY) engine/render.py examples/slides/slide_2_useful_drop.html  $(DEMO)/slide_2.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/slide_3_stack_diagram.html $(DEMO)/slide_3.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/slide_4_comparison.html    $(DEMO)/slide_4.png --size $(SIZE) --brand-css $(BRAND)
	# --- template path (basic): a stat slide with a real ECharts bar, and the CTA ---
	$(PY) engine/graphics_templates.py stat examples/copy/stat.json $(DEMO)/slide_5.html --size $(SIZE) --pager "05 / 06"
	$(PY) engine/render.py $(DEMO)/slide_5.html $(DEMO)/slide_5.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/graphics_templates.py cta examples/copy/cta.json $(DEMO)/slide_6.html --size $(SIZE) --pager "06 / 06"
	$(PY) engine/render.py $(DEMO)/slide_6.html $(DEMO)/slide_6.png --size $(SIZE) --brand-css $(BRAND)
	@echo "Demo carousel rendered -> $(DEMO)/slide_1.png ... slide_6.png"

# 3) Regenerate the committed reference gallery (advanced-path layout showcase + statement template).
examples: css
	@mkdir -p examples/expected
	# the 6 carousel frames
	$(PY) engine/graphics_templates.py cover examples/copy/cover.json examples/expected/slide_1_cover.html --size $(SIZE) --pager "01 / 06"
	$(PY) engine/render.py examples/expected/slide_1_cover.html examples/expected/slide_1_cover.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/slide_2_useful_drop.html  examples/expected/slide_2_useful_drop.png  --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/slide_3_stack_diagram.html examples/expected/slide_3_stack_diagram.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/slide_4_comparison.html    examples/expected/slide_4_comparison.png    --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/graphics_templates.py stat examples/copy/stat.json examples/expected/slide_5_stat.html --size $(SIZE) --pager "05 / 06"
	$(PY) engine/render.py examples/expected/slide_5_stat.html examples/expected/slide_5_stat.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/graphics_templates.py cta examples/copy/cta.json examples/expected/slide_6_cta.html --size $(SIZE) --pager "06 / 06"
	$(PY) engine/render.py examples/expected/slide_6_cta.html examples/expected/slide_6_cta.png --size $(SIZE) --brand-css $(BRAND)
	# the statement template (basic path)
	$(PY) engine/graphics_templates.py statement examples/copy/statement.json examples/expected/tpl_statement.html --size $(SIZE)
	$(PY) engine/render.py examples/expected/tpl_statement.html examples/expected/tpl_statement.png --size $(SIZE) --brand-css $(BRAND)
	# the advanced-path layout gallery
	$(PY) engine/render.py examples/slides/gallery_progression.html      examples/expected/gallery_progression.png      --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_matrix.html           examples/expected/gallery_matrix.png           --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_myth_reframe.html     examples/expected/gallery_myth_reframe.png     --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_problem_solution.html examples/expected/gallery_problem_solution.png --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_steps.html            examples/expected/gallery_steps.png            --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_list.html             examples/expected/gallery_list.png             --size $(SIZE) --brand-css $(BRAND)
	$(PY) engine/render.py examples/slides/gallery_quote.html            examples/expected/gallery_quote.png            --size $(SIZE) --brand-css $(BRAND)
	@rm -f examples/expected/*.html
	@echo "Reference gallery rendered -> examples/expected/*.png"

clean:
	rm -rf out

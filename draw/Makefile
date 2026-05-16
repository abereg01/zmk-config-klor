# ===========================================================================
# KLOR keymap-drawer  —  generates base.svg, overview.svg, keymap.png
#
# Usage (run from the draw/ directory, or from repo root with -C draw):
#
#   make                  — build all outputs (Gruvbox theme)
#   make THEME=nord       — Nord theme
#   make THEME=dracula    — Dracula theme
#   make THEME=gruvbox    — explicit Gruvbox
#   make base.svg         — BASE layer only
#   make overview.svg     — all layers
#   make keymap.png       — PNG export of overview (requires cairosvg)
#   make clean            — remove generated SVG/PNG outputs (keeps klor.yaml)
#   make clean-all        — remove everything including klor.yaml
#
# Available themes: gruvbox  nord  dracula
# Add a new theme by creating draw/themes/<name>.yaml, then: make THEME=<name>
#
# Requirements:
#   pip install keymap-drawer cairosvg
#
# The PNG step strips CSS block-comments from the SVG first because cairosvg
# parses SVG as strict XML and rejects them.  All other steps are unaffected.
# ===========================================================================

KEYMAP    := ../config/boards/shields/klor/klor.keymap
BASE_CFG  := keymap-drawer.yaml
THEME     ?= gruvbox
THEME_CFG := themes/$(THEME).yaml
MERGED    := /tmp/klor-$(THEME).yaml
SCALE     := 2        # PNG export scale factor  (2 = ~192 dpi)

.PHONY: all clean clean-all

all: base.svg overview.svg keymap.png

# ---------------------------------------------------------------------------
# 1. Merge base config + theme  →  temp merged config
#    Parse uses BASE_CFG directly (no theme needed for parsing).
#    Draw steps use MERGED so colours come from the selected theme.
# ---------------------------------------------------------------------------
$(MERGED): $(BASE_CFG) $(THEME_CFG) merge-theme.py
	python3 merge-theme.py $(BASE_CFG) $(THEME_CFG) > $(MERGED)

# ---------------------------------------------------------------------------
# 2. Parse the ZMK keymap into an intermediate YAML representation
# ---------------------------------------------------------------------------
klor.yaml: $(KEYMAP) $(BASE_CFG)
	keymap -c $(BASE_CFG) parse -z $(KEYMAP) > $@

# ---------------------------------------------------------------------------
# 3. BASE layer only  →  base.svg
#    Layer names from ZMK parse come out lowercase ("base", "lower", etc.)
# ---------------------------------------------------------------------------
base.svg: klor.yaml $(MERGED)
	keymap -c $(MERGED) draw $< -s base > $@

# ---------------------------------------------------------------------------
# 4. All layers  →  overview.svg
# ---------------------------------------------------------------------------
overview.svg: klor.yaml $(MERGED)
	keymap -c $(MERGED) draw $< > $@

# ---------------------------------------------------------------------------
# 5. PNG export  →  keymap.png
#    cairosvg parses SVG as XML and rejects CSS block-comments, so we strip
#    them with sed before piping in.
# ---------------------------------------------------------------------------
keymap.png: overview.svg
	sed 's|/\*[^*]*\*\+\([^/][^*]*\*\+\)*/||g' $< \
	  | python3 -m cairosvg - -f png -o $@ --scale $(SCALE)

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
clean:
	rm -f base.svg overview.svg keymap.png $(MERGED)

clean-all: clean
	rm -f klor.yaml

KEYMAP := ../config/boards/shields/klor/klor.keymap
CFG    := keymap-drawer.yaml

.PHONY: all clean

all: base.svg overview.svg

klor.yaml: $(KEYMAP) $(CFG)
	keymap -c $(CFG) parse -z $(KEYMAP) > $@

base.svg: klor.yaml $(CFG)
	keymap -c $(CFG) draw $< -s BASE > $@

overview.svg: klor.yaml $(CFG)
	keymap -c $(CFG) draw $< > $@

keymap.png: overview.svg
	python3 -m cairosvg $< -f png -o $@ --scale 2

clean:
	rm -f klor.yaml base.svg overview.svg keymap.png

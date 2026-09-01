MAIN=main.tex
BUILD=build

.PHONY: draft release clean

draft:
	mkdir -p $(BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) $(MAIN)
	xelatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) $(MAIN)

release: draft
	cp $(BUILD)/main.pdf $(BUILD)/release.pdf

clean:
	rm -f $(BUILD)/*

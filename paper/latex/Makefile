PYTHON ?= python3
PROFILE ?= generic
ENGINE ?= xelatex
TIMEOUT ?= 180

.PHONY: draft review release print all clean help

draft:
	$(PYTHON) build.py draft --profile $(PROFILE) --engine $(ENGINE) --timeout $(TIMEOUT)

review:
	$(PYTHON) build.py review --profile $(PROFILE) --engine $(ENGINE) --timeout $(TIMEOUT)

release:
	$(PYTHON) build.py release --profile $(PROFILE) --engine $(ENGINE) --timeout $(TIMEOUT)

print:
	$(PYTHON) build.py print --profile $(PROFILE) --engine $(ENGINE) --timeout $(TIMEOUT)

all:
	$(PYTHON) build.py all --profile $(PROFILE) --engine $(ENGINE) --timeout $(TIMEOUT)

clean:
	$(PYTHON) build.py clean

help:
	@echo "make draft|review|release|print|all|clean"
	@echo "Optional: PROFILE=generic ENGINE=xelatex TIMEOUT=180"

PYTHON ?= python3

.PHONY: screenshots check refresh-data

## Regenerate every screenshot from terminal/scripts/*.ts
screenshots:
	rm -f screenshots/*.svg terminal/output/*.txt
	$(PYTHON) scripts/termscript.py terminal/scripts/*.ts

## Check that chapters and capture scripts agree on screenshots
check:
	$(PYTHON) scripts/check_screenshots.py

## Deliberately re-download the dataset the screenshots are captured from
refresh-data:
	curl -sSf "https://api.nobelprize.org/2.1/nobelPrizes?limit=1000" -o datasets/prizes.json

PYTHON ?= python3

.DEFAULT_GOAL := all
.PHONY: all engineering legal memo presentation marking-demos \
	synthetic-confidential synthetic-ear synthetic-itar synthetic-secret \
	synthetic-top-secret check test clean

all:
	$(PYTHON) scripts/build.py all

engineering legal memo presentation:
	$(PYTHON) scripts/build.py $@

marking-demos synthetic-confidential synthetic-ear synthetic-itar synthetic-secret synthetic-top-secret:
	$(PYTHON) scripts/build.py $@

check:
	$(PYTHON) scripts/build.py --check

test:
	$(PYTHON) scripts/build.py --test

clean:
	$(PYTHON) scripts/build.py --clean

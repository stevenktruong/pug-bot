# Settings
PIP = pip3
PYTHON = python3

init:
	$(PIP) install -r requirements.txt

start:
	$(shell $(PYTHON) main.py >&2)

.PHONY: init start

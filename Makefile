# Settings
PIP = pip3
PYTHON = python3

init:
	$(PIP) install -r requirements.txt

start:
	$(PYTHON) main.py

.PHONY: init start

# Settings
PIP = pip

all: init

init:
	$(PIP) install -r requirements.txt

.PHONY: init

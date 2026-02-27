.PHONY: install demo clean

VENV := .venv
PIP := uv pip
PYTHON := $(VENV)/bin/python

install:
	$(PIP) install -r requirements.txt

demo:
	PYTHONPATH=lib $(PYTHON) lib/pagecraft/examples/demo.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f lib/pagecraft/examples/demo_output.pdf

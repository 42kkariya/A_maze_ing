VENV    := .venv
PYTHON  := $(VENV)/bin/python
CONFIG  := config.txt

all: run

$(PYTHON):
	python3 -m venv $(VENV)

install: $(PYTHON)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

test:
	$(PYTHON) -m pytest tests

build:
	$(PYTHON) -m build
	cp dist/mazegen-*.whl .

clean:
	find . -path ./$(VENV) -prune -o -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

fclean: clean
	rm -rf $(VENV) mazegen-*.whl mazegen-*.tar.gz

analyze:
	$(PYTHON) tools/maze_analyzer.py maze.txt

.PHONY: all install run debug lint lint-strict test build clean fclean analyze

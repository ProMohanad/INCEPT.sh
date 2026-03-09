.PHONY: all lint format typecheck test serve benchmark smoke

all: lint typecheck test

## Development
lint:
	python -m ruff check incept/ tests/

format:
	python -m ruff format incept/ tests/

typecheck:
	python -m mypy incept/

test:
	python -m pytest tests/ -v --tb=short

## Runtime
serve:
	python -m incept.cli.main serve

benchmark:
	python -m incept.training.benchmark

smoke:
	python -m incept.cli.main -c "list files in current directory"

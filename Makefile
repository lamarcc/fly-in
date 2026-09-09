isntall:
	uv sync

run:
	uv run src/main.py

lint:
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

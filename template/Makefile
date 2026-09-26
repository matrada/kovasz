.PHONY: init test check clean

init:
	uv sync
	uv run pre-commit install

test:
	uv run pytest

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest

clean:
	rm -rf .venv __pycache__ .ruff_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# ModernPowley -- canonical command surface. See AGENTS.md for what each
# step means and why; this file only sequences them.

default:
    @just --list

# Stdlib-only and run with the system interpreter on purpose: it must work
# before `uv sync`, since it decides whether this checkout is current.
freshness:
    python3 scripts/freshness.py

setup:
    uv sync --locked

check: setup
    uv run pytest -q
    uv run python -m compileall -q src scripts tests
    uv lock --check
    git diff --check
    uv run ruff check .

typecheck:
    uv run mypy src

audit:
    uv run python scripts/audit_regression.py
    uv run python scripts/generate_audit_inventory.py

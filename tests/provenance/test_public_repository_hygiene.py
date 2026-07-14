import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "jupyter/demo.ipynb"
PERSONAL_HOME = re.compile(
    r"(?:/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|"
    r"[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+[\\/])"
)


def _check_ignore(path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "check-ignore", "--no-index", path],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _execution_metadata_keys(value: object) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = key.lower()
            if key == "execution" or (
                "execution" in lowered and ("time" in lowered or "timestamp" in lowered)
            ):
                keys.append(key)
            keys.extend(_execution_metadata_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(_execution_metadata_keys(child))
    return keys


def test_gitignore_is_multiline_and_contains_repository_hygiene_policy():
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    required = {
        "__pycache__/",
        ".pytest_cache/",
        ".venv/",
        ".uv-cache/",
        "build/",
        ".ipynb_checkpoints/",
        ".env",
        "!.env.example",
        "/cartridge_db.sqlite",
        "*.sqlite-wal",
        "id_ed25519",
        ".codex/",
    }
    assert required <= set(lines)
    assert len(lines) > len(required) * 4
    assert all(len(line) < 120 for line in lines)
    assert not {"*.csv", "*.json", "*.md", "*.pdf", "*.html", "*.ipynb"} & set(lines)


def test_authoritative_files_are_not_ignored():
    paths = (
        "uv.lock",
        ".python-version",
        "pyproject.toml",
        "AGENTS.md",
        "jupyter/demo.ipynb",
        "reference/source_ledger.csv",
        "docs/provenance/equation_ledger.csv",
        "data/reference/davis_1981_table4.csv",
        "reference/powley_manual/powleysmanuals1.pdf",
        "reference/online_emulator/kwk_powley_20240228.html",
    )
    for path in paths:
        result = _check_ignore(path)
        assert result.returncode == 1, (path, result.stdout, result.stderr)


def test_notebook_is_sanitized_but_retains_audit_warning():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    serialized = json.dumps(notebook)
    assert PERSONAL_HOME.search(serialized) is None

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert code_cells
    assert all(cell.get("outputs") == [] for cell in code_cells)
    assert all(cell.get("execution_count") is None for cell in code_cells)
    assert _execution_metadata_keys(notebook) == []

    sources = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
    assert any(
        'raise RuntimeError("Legacy notebook disabled by provenance audit; see README.md")'
        in source
        for source in sources
    )
    assert any("stale, invalid legacy notebook" in source for source in sources)
    assert any("not measurement evidence" in source for source in sources)
    assert any("pre_audit_agent_derived_prototype" in source for source in sources)

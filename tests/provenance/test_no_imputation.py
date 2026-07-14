from pathlib import Path


def test_canonical_package_contains_no_mean_imputation():
    source = Path("src/modern_powley")
    text = "\n".join(path.read_text() for path in source.rglob("*.py"))
    assert "fillna" not in text

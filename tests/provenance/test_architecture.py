import ast
from pathlib import Path


def test_original_namespace_has_no_experimental_later_modernized_or_grt_imports():
    forbidden_parts = {"experimental", "later", "modernized", "grt", "parse_grt_cartridge", "parse_grt_prop"}
    for path in Path("src/modern_powley/original").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
                imported.extend(alias.name for alias in node.names)
        assert not [
            name for name in imported if forbidden_parts.intersection(name.replace("-", "_").split("."))
        ], path


def test_modernized_imports_original_only_through_explicit_adapter():
    for path in Path("src/modern_powley/modernized").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        original_imports = [name for name in imported if name.startswith("modern_powley.original")]
        if original_imports:
            assert path.as_posix().endswith("modernized/adapters/original.py"), path
        assert not [name for name in imported if name.startswith(("modern_powley.later", "modern_powley.experimental"))], path


def test_m01_canonical_api_has_no_ambiguous_or_later_phase_symbols():
    import modern_powley.modernized as modernized

    public = set(modernized.__all__)
    assert not public & {
        "expansion_ratio", "loading_density", "case_volume", "effective_case_volume",
        "select_powder", "estimate_pressure", "estimate_velocity", "burnout", "muzzle_pressure",
        "Ba_eff", "Ba_target", "optimal_charge", "recommend",
    }

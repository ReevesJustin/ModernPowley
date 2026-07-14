import ast
from pathlib import Path


def test_original_namespace_has_no_experimental_later_or_grt_imports():
    forbidden_parts = {"experimental", "later", "grt", "parse_grt_cartridge", "parse_grt_prop"}
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

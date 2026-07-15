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
    forbidden_import_prefixes = (
        "modern_powley.later",
        "modern_powley.experimental",
        "scripts.",
    )
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
        assert not [name for name in imported if name.startswith(forbidden_import_prefixes)], path


def test_m01_canonical_api_has_no_ambiguous_or_later_phase_symbols():
    import modern_powley.modernized as modernized

    public = set(modernized.__all__)
    assert not public & {
        "expansion_ratio", "loading_density", "case_volume", "effective_case_volume",
        "select_powder", "estimate_pressure", "estimate_velocity", "burnout", "muzzle_pressure",
        "Ba_eff", "Ba_target", "optimal_charge", "recommend",
    }


def test_m02_public_api_has_no_selection_prediction_or_resolution_behavior():
    import modern_powley.modernized as modernized

    public = set(modernized.__all__)
    prohibited = {
        "screen_powders", "select_powder", "selected_powder", "rank_powders",
        "recommend", "recommended_value", "preferred_record", "best_property",
        "effective_property", "default_powder", "resolve_conflict",
        "interpolate_property", "extrapolate_property", "complete_property",
        "estimate_charge", "estimate_pressure", "estimate_velocity",
        "calculate_energy_release", "burnout", "muzzle_pressure", "solver",
    }
    assert not public & prohibited


def test_m02_modules_define_only_contract_domain_and_descriptive_comparison_calls():
    prohibited_definitions = {
        "screen", "select", "rank", "recommend", "resolve", "interpolate",
        "extrapolate", "predict", "optimize", "solve", "impute",
    }
    m02_files = (
        "powder_identity.py", "powder_properties.py", "property_domains.py",
        "missing_values.py", "property_observations.py", "property_conflicts.py",
        "m02_serialization.py",
    )
    for name in m02_files:
        path = Path("src/modern_powley/modernized") / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        definitions = {
            node.name.casefold()
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        assert not {
            item for item in definitions
            if any(token in item for token in prohibited_definitions)
        }, path


def test_m03_public_api_has_no_screening_selection_prediction_or_solver_names():
    import modern_powley.modernized as modernized

    prohibited = {
        "screen_powders", "eligible_powders", "suitable_powders", "rank_candidates",
        "recommended_inputs", "solver_ready", "load_ready", "effective_capacity",
        "preferred_observation", "best_record", "select_property", "default_geometry",
        "estimate_pressure", "estimate_velocity", "charge_predictor",
    }
    assert prohibited.isdisjoint(set(modernized.__all__))


def test_m03_modules_define_only_requirements_and_literal_diagnostics():
    prohibited_definitions = {
        "screen", "select", "rank", "recommend", "interpolate", "extrapolate",
        "predict", "optimize", "solve", "calibrate", "impute", "infer",
    }
    m03_files = (
        "input_requirements.py", "input_completeness.py",
        "domain_diagnostics.py", "m03_serialization.py",
    )
    for name in m03_files:
        path = Path("src/modern_powley/modernized") / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        definitions = {
            node.name.casefold()
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        assert not {
            item for item in definitions
            if any(token in item for token in prohibited_definitions)
        }, path


def test_m05_modules_are_records_and_serialization_only():
    prohibited = {
        "estimate", "derive", "intersect", "union", "normalize", "merge",
        "rank", "recommend", "select", "round", "propagate", "simulate",
        "predict", "calculate", "parse_grt", "plot", "upload",
    }
    for name in ("charge_regions.py", "m05_serialization.py"):
        path = Path("src/modern_powley/modernized") / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        public_definitions = {
            node.name.casefold()
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not node.name.startswith("_")
        }
        assert not {
            item for item in public_definitions
            if any(token in item for token in prohibited)
        }, path


def test_m05_has_no_forbidden_namespace_dependencies():
    forbidden = {"original", "later", "experimental", "emulator", "grt", "jrt", "quickload", "scripts", "plot", "web"}
    for name in ("charge_regions.py", "m05_serialization.py"):
        path = Path("src/modern_powley/modernized") / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        assert not [item for item in imported if forbidden.intersection(item.casefold().split("."))], path

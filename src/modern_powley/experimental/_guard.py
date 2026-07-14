def require_opt_in(allow_unvalidated: bool) -> None:
    if allow_unvalidated is not True:
        raise RuntimeError("unvalidated ModernPowley experiment requires allow_unvalidated=True")

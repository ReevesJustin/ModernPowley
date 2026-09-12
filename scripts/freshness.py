#!/usr/bin/env python3
"""Verify this checkout against its upstream and fast-forward only when safe.

This is a once-per-agent-session repository lifecycle gate, not validation.
It fetches remote refs, never pushes or changes configuration, and modifies the
checkout only when the current branch is clean and strictly behind upstream.

It also fetches every other configured remote (e.g. a second mirror) and stops
if any holds a commit this checkout lacks, even when the tracked upstream is
current -- a soft safeguard against acting on stale policy when a repo has
more than one authoritative remote.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class FreshnessError(RuntimeError):
    """A state in which repository freshness cannot be established safely."""


def _git(*args: str, timeout: int = 15) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise FreshnessError(f"git {' '.join(args)} timed out") from exc
    except OSError as exc:
        raise FreshnessError(f"cannot run git: {exc}") from exc


def _command_detail(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stderr or result.stdout).strip() or f"exit {result.returncode}"


def _branch() -> str:
    result = _git("symbolic-ref", "--quiet", "--short", "HEAD")
    if result.returncode == 1:
        raise FreshnessError(
            "detached HEAD; check out a branch with a configured upstream "
            "before modifying the repository"
        )
    if result.returncode != 0:
        raise FreshnessError(f"cannot determine current branch: {_command_detail(result)}")
    return result.stdout.strip()


def _upstream(branch: str) -> tuple[str, str]:
    upstream_result = _git(
        "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"
    )
    if upstream_result.returncode != 0:
        raise FreshnessError(
            f"branch '{branch}' has no configured upstream; freshness cannot be verified"
        )
    upstream = upstream_result.stdout.strip()

    remote_result = _git("config", "--get", f"branch.{branch}.remote")
    remote = remote_result.stdout.strip()
    if remote_result.returncode != 0 or not remote:
        raise FreshnessError(
            f"branch '{branch}' has an upstream but no resolvable remote configuration"
        )
    return upstream, remote


def _remotes() -> list[str]:
    result = _git("remote")
    if result.returncode != 0:
        raise FreshnessError(f"cannot inspect configured remotes: {_command_detail(result)}")
    return [line for line in result.stdout.splitlines() if line]


def _counts(upstream: str) -> tuple[int, int]:
    result = _git("rev-list", "--left-right", "--count", f"HEAD...{upstream}")
    if result.returncode != 0:
        raise FreshnessError(
            f"cannot compare HEAD with '{upstream}': {_command_detail(result)}"
        )
    try:
        ahead, behind = (int(value) for value in result.stdout.split())
    except (TypeError, ValueError) as exc:
        raise FreshnessError(f"unexpected comparison output: {result.stdout!r}") from exc
    return ahead, behind


def _dirty() -> bool:
    result = _git("status", "--porcelain=v1", "--untracked-files=normal")
    if result.returncode != 0:
        raise FreshnessError(f"cannot inspect working tree: {_command_detail(result)}")
    return bool(result.stdout)


def _remote_branch_counts(remote: str, branch: str) -> tuple[int, int] | None:
    """Ahead/behind HEAD vs. `<remote>/<branch>`, or None if that ref doesn't exist."""
    ref = f"{remote}/{branch}"
    exists = _git("rev-parse", "--verify", "--quiet", ref)
    if exists.returncode != 0:
        return None
    return _counts(ref)


def _check_other_remotes(branch: str, remotes: list[str], tracked_remote: str) -> None:
    """Fail if any non-tracked remote holds a commit this checkout lacks.

    Template-project's own policy (ADRs, skills, contracts) lives in its git
    history. A checkout can be current against its tracked upstream while a
    second remote (e.g. a mirror pushed to directly) has already moved ahead
    -- this is a soft safeguard against silently acting on stale policy in
    that case, not a general multi-remote sync tool.
    """
    for remote in remotes:
        if remote == tracked_remote:
            continue
        fetch = _git("fetch", "--quiet", "--no-tags", remote, timeout=60)
        if fetch.returncode != 0:
            raise FreshnessError(
                f"fetch from '{remote}' failed; freshness relative to it is unknown: "
                f"{_command_detail(fetch)}"
            )
        counts = _remote_branch_counts(remote, branch)
        if counts is None:
            continue
        _ahead, behind = counts
        if behind > 0:
            raise FreshnessError(
                f"remote '{remote}' has {behind} commit(s) on '{branch}' not present "
                f"locally or on the tracked upstream; resolve explicitly before continuing"
            )


def check_freshness() -> None:
    branch = _branch()
    remotes = _remotes()
    if not remotes:
        print(f"freshness: local-only ({branch}; no remotes configured)")
        return
    upstream, remote = _upstream(branch)

    fetch = _git("fetch", "--quiet", "--no-tags", remote, timeout=60)
    if fetch.returncode != 0:
        raise FreshnessError(
            f"fetch from '{remote}' failed; freshness is unknown: {_command_detail(fetch)}"
        )

    _check_other_remotes(branch, remotes, remote)

    ahead, behind = _counts(upstream)
    if ahead == 0 and behind == 0:
        print(f"freshness: current ({branch} == {upstream})")
        return
    if ahead > 0 and behind == 0:
        print(
            f"freshness: local branch '{branch}' is ahead of '{upstream}' by "
            f"{ahead} commit(s); continue, but local commits are unpushed"
        )
        return
    if ahead > 0 and behind > 0:
        raise FreshnessError(
            f"branch '{branch}' and '{upstream}' have diverged "
            f"({ahead} local, {behind} upstream commit(s)); resolve explicitly"
        )
    if _dirty():
        raise FreshnessError(
            f"branch '{branch}' is behind '{upstream}' by {behind} commit(s), "
            "but the working tree is dirty; resolve local work explicitly before retrying"
        )

    pull = _git("pull", "--ff-only", "--no-rebase", timeout=120)
    if pull.returncode != 0:
        raise FreshnessError(
            f"fast-forward from '{upstream}' failed: {_command_detail(pull)}"
        )

    branch_after = _branch()
    upstream_after, _remote_after = _upstream(branch_after)
    ahead_after, behind_after = _counts(upstream_after)
    if branch_after != branch or upstream_after != upstream:
        raise FreshnessError("branch or upstream changed during fast-forward; stop and inspect")
    if ahead_after != 0 or behind_after != 0:
        raise FreshnessError(
            f"fast-forward did not reach '{upstream}' "
            f"({ahead_after} ahead, {behind_after} behind)"
        )
    if _dirty():
        raise FreshnessError("fast-forward completed but the working tree is not clean")
    print(f"freshness: fast-forwarded '{branch}' to '{upstream}' and revalidated")


def main() -> int:
    try:
        check_freshness()
    except FreshnessError as exc:
        print(f"freshness: error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

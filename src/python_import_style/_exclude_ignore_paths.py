# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Preprocess a list of paths to exclude files ignored by git."""

import pathlib
import subprocess


def _exclude_ignore_paths(
    project_root: pathlib.Path, paths: list[pathlib.Path]
) -> list[pathlib.Path]:
    """Preprocess `paths` to exclude files ignored by git."""
    assert all(p.is_absolute() for p in paths)
    rel_paths = [p.relative_to(project_root) for p in paths]
    input_bytes = "\0".join(str(p) for p in rel_paths).encode("utf-8")
    print(rel_paths, input_bytes)
    proc = subprocess.run(
        ["git", "check-ignore", "-z", "--stdin"],
        input=input_bytes,
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    ignored: set[pathlib.Path] = set()
    if proc.returncode == 0:  # One or more of the provided paths is ignored
        for raw in proc.stdout.strip(b"\0").split(b"\0"):
            ignored_rel_path = pathlib.Path(raw.decode("utf-8"))
            assert ignored_rel_path in rel_paths, (
                f"Unexpected ignored path: {ignored_rel_path}"
            )
            assert (project_root / ignored_rel_path).exists(), (
                f"Git ignored path does not exist: {ignored_rel_path}"
            )
            ignored.add(ignored_rel_path)
    elif proc.returncode == 1:  # None of the provided paths are ignored.
        pass
    else:
        stdout = proc.stdout.decode("utf-8") if proc.stdout else "empty"
        stderr = proc.stderr.decode("utf-8") if proc.stderr else "empty"
        raise RuntimeError(
            f"Git check-ignore failed with return code {proc.returncode}, "
            f"stdout: {stdout} and stderr: {stderr}"
        )
    return [project_root / p for p in rel_paths if p not in ignored]

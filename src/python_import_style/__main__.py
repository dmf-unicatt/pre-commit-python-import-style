# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""CLI entrypoint for the package."""

import argparse
import pathlib
import sys

import python_import_style


def _main(argv: list[str]) -> int:
    """CLI entrypoint. Returns an exit code (0 success, 1 failure)."""
    parser = argparse.ArgumentParser(
        description="Check Python import style for package and tests folders."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="File list provided by prek.",
    )
    parser.add_argument(
        "--root-dir",
        default=".",
        help="Project root directory (default: current directory).",
    )
    parser.add_argument(
        "--package-dir-prefix",
        default=".",
        help=(
            "Parent directory of the package, relative to the project root "
            "(default: empty)."
        ),
    )
    parser.add_argument(
        "--package-name",
        required=True,
        help="Package name to validate.",
    )
    parser.add_argument(
        "--tests-dir",
        default="tests",
        help="Tests directory to validate (default: tests).",
    )
    args = parser.parse_args(argv)

    project_root = pathlib.Path(args.root_dir).absolute()
    package_root = project_root / args.package_dir_prefix / args.package_name
    tests_root = project_root / args.tests_dir
    file_paths = [
        pathlib.Path(project_root / file_name) for file_name in args.files
    ]

    errors = python_import_style.check_all_rules(
        args.package_name, project_root, package_root, tests_root, file_paths
    )

    if errors:
        for error in errors:
            print(error)
        return 1
    else:  # pragma: no cover
        return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))

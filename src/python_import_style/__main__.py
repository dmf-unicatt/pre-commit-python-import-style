# Copyright (C) 2026 by Francesco Ballarin
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Entrypoint for the python_import_style package."""

import argparse
import pathlib
import sys

import python_import_style


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Build and return the CLI argument parser namespace."""
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint. Returns an exit code (0 success, 1 failure)."""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    root_dir = pathlib.Path(args.root_dir).resolve()
    files = [pathlib.Path(file_name).resolve() for file_name in args.files]

    errors = python_import_style.run_checks(
        files=files,
        root_dir=root_dir,
        package_dir_prefix=args.package_dir_prefix,
        package_name=args.package_name,
        tests_dir_name=args.tests_dir,
    )

    if errors:
        print("Import style violations found:")
        for error in errors:
            print(error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

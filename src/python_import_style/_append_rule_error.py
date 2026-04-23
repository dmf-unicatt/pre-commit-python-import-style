# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Append a formatted rule violation message to a list of strings."""

import pathlib


def _append_rule_error(
    errors: list[str],
    file_path: pathlib.Path,
    lineno: int,
    rule_number: int | None,
    message: str,
) -> None:
    """Append a formatted rule violation message to `errors`.

    The format matches the project's tests (file:lineno -> Rule N: message).
    """
    full_message = f"{file_path}:{lineno} -> "
    if rule_number is not None:
        full_message += f"Rule {rule_number}: "
    else:
        full_message += "Error: "
    full_message += message
    errors.append(full_message)

"""Shared feature group: validated JSON loading and safe replacement (AI-authored)."""

import json
import os
from pathlib import Path
import tempfile

from engineer_a.tickets import validate_records


class StorageError(ValueError):
    """A persistence failure that the CLI can display without a traceback."""


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}.")
        result[key] = value
    return result


def load_tickets(path):
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as handle:
            tickets = json.load(handle, object_pairs_hook=_unique_keys)
        return validate_records(tickets)
    except FileNotFoundError:
        return []
    except (OSError, UnicodeError, ValueError) as error:
        raise StorageError(f"Cannot load {path}: {error} Existing data has not been changed.") from error


def save_tickets(tickets, path):
    """Validate first, then write and fsync a sibling file before replacing.

An existing malformed file is protected even when this function is called
directly. There is no multi-process locking; run one instance per data file.
"""
    path = Path(path)
    temporary_path = None
    try:
        validate_records(tickets)
        # Refuse to overwrite a damaged file that appeared after startup.
        load_tickets(path)
        payload = json.dumps(tickets, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except (OSError, UnicodeError, ValueError) as error:
        raise StorageError(f"Cannot save {path}: {error}") from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

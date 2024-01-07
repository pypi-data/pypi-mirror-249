import logging
import os
from typing import Any, Optional

from bib2tex.file_handler import read_json_file
from bib2tex.config import (
    COL_ENTRYTYPE,
    CT_KEY_BIBTEXTYPE,
    CT_KEY_FORMATSCHEMES,
    CT_KEY_SEARCHSTRINGS,
)
from bib2tex.bibtex_filter import filter_by_key
from bib2tex.format_schemes import FormatSchemeManager

CUSTOM_TYPE_KEYS_REQUIRED = [
    CT_KEY_BIBTEXTYPE,
    CT_KEY_FORMATSCHEMES,
    CT_KEY_SEARCHSTRINGS,
]

custom_entrytypes: dict[str, dict[str, Any]] = {}


class CustomTypeError(Exception):
    pass


def register_custom_types(
    file_path: str, format_scheme_manager: FormatSchemeManager
) -> None:
    """Add custom BibTeX based entrytypes from a JSON file."""

    definitions = read_json_file(file_path)
    if not isinstance(definitions, dict):
        raise CustomTypeError("Custom type definitions must be a dictionary.")
    logging.debug(f"Loaded custom entry type definitions from {file_path!r}.")

    for entry_type, tdefs in definitions.items():
        # ensure required keys are present
        missing_keys = set(CUSTOM_TYPE_KEYS_REQUIRED) - set(tdefs.keys())
        if missing_keys:
            missing_keys_str = ", ".join(repr(key) for key in missing_keys)
            raise KeyError(
                f"Required definitions {missing_keys_str} not provided for custom entry type {entry_type!r}."
            )

        # register format scheme
        for fsname, format_scheme in definitions[entry_type][
            CT_KEY_FORMATSCHEMES
        ].items():
            format_scheme_manager.add_format_scheme(fsname, entry_type, format_scheme)

    custom_entrytypes.update(definitions)
    logging.debug(f"Registered custom entry type definitions.")


def get_custom_type_names() -> list[str]:
    """Get names of registered custom entry types."""
    return list(custom_entrytypes.keys())


def get_entries_for_custom_type(
    entries: list[dict[str, Any]], entry_type: str
) -> list[dict[str, Any]]:
    """Filter BibTeX entries for a custom entry type."""
    ctype_defs = custom_entrytypes[entry_type]

    # find custom types in subset of entries
    bt_entries = filter_by_key(entries, COL_ENTRYTYPE, ctype_defs[CT_KEY_BIBTEXTYPE])
    ct_entries = []
    for s_field, s_value in ctype_defs[CT_KEY_SEARCHSTRINGS].items():
        ct_entries += filter_by_key(bt_entries, s_field, s_value)

    # replace BibTeX type with custom type
    for entry in ct_entries:
        entry[COL_ENTRYTYPE] = entry_type

    return ct_entries

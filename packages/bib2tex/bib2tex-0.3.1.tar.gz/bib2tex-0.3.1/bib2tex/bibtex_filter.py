from typing import Any, Optional

from bib2tex.config import COL_ENTRYTYPE, LATEX_INDENT


def month_to_number(month: str) -> int:
    """Convert a three-letter month abbreviation to its numeric representation."""
    months_mapping = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    try:
        return months_mapping.get(month.lower(), 0)
    except:
        return 0


def sort_entries(
    input_list: list[dict[str, Any]],
    primary_key: str = "year",
    secondary_key: str = "month",
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Sort a entries based on year and month key."""
    if secondary_key is not ("month" or None):
        raise KeyError(f'Secondary sort key must be "month" or None.')
    return sorted(
        input_list,
        key=lambda x: (
            x.get(primary_key, ""),
            month_to_number(x.get(secondary_key, None)) if secondary_key else None,
        ),
        reverse=reverse,
    )


def filter_by_key(
    entries: list[dict[str, Any]], key: str, value: str, case_sensitive=True
) -> list[dict[str, Any]]:
    """Filter a list of dictionaries based on a key-value pair.

    The check is whether the provided value is a substring of the dict's
    value for the specified key in the entries, not if they are equal.
    """

    def is_value_present(entry):
        entry_value = str(entry.get(key, ""))
        return (
            value in entry_value
            if case_sensitive
            else value.lower() in entry_value.lower()
        )

    return [entry for entry in entries if key in entry and is_value_present(entry)]


def filter_entries(
    entries: list[dict[str, Any]],
    author: str,
    entrytype: Optional[str],
    reverse=False,
    case_sensitive=False,
) -> list[dict[str, Any]]:
    """Filter BibTeX entries for author (and entrytype).

    Entries are returned sorted by year and month. The newest entry
    will be on top, set reverse to True to have it at the bottom.
    """
    result = filter_by_key(entries, "author", author, case_sensitive=case_sensitive)
    if entrytype and len(result) > 0:
        result = filter_by_key(result, COL_ENTRYTYPE, entrytype)
    # inversion of reverse since the default should be new (top) to old (bottom),
    # but the functions uses sorted, which sorts in ascending order if not revered
    # (smaller to larger years).
    return sort_entries(result, reverse=not reverse)

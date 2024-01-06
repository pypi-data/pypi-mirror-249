import logging
import sys
from typing import Any, Optional

from bib2tex.config import (
    COL_ENTRYTYPE,
    COL_CITATIONKEY,
    COL_NAME_FULL,
    COL_NAME_FIRST,
    COL_NAME_LAST,
    ENCODING,
)


def parse_author_str(author_str: str) -> list[dict[str, Optional[str]]]:
    """Parse a BibTeX author string into a list of dictionaries.

    Args:
        author_str (str): BibTeX author string.

    Returns:
        list[dict[str, str | None]]: List of dictionaries representing author names.
    """
    fullname, lastname, firstname = None, None, None
    author_dicts: list[dict[str, str | None]] = []
    if " and " in author_str:
        authors = author_str.split(" and ")
        for author in authors:
            if ", " in author:
                try:
                    lastname, firstname = author.split(", ")
                    fullname = f"{firstname} {lastname}"
                except ValueError:
                    logging.error(
                        f"Value error occured while parsing author string ({author!r}), aborted."
                    )
                    sys.exit()
            else:
                fullname = author
                if len(fullname.split()) == 2:
                    firstname, lastname = fullname.split()
            author_dict = {
                COL_NAME_FULL: fullname,
                COL_NAME_FIRST: firstname,
                COL_NAME_LAST: lastname,
            }
            author_dicts.append(author_dict)
        return author_dicts
    # Single author paper...
    if author_str.count(", ") == 1:
        lastname, firstname = author_str.split(", ")
        fullname = f"{firstname} {lastname}"
    else:
        fullname = author_str
        if author_str.count(" ") > 1:
            logging.warning(
                f"Author not conform with the BibTeX name format: {author_str!r}"
            )
    author_dict = {
        COL_NAME_FULL: fullname,
        COL_NAME_FIRST: firstname,
        COL_NAME_LAST: lastname,
    }
    author_dicts.append(author_dict)
    return author_dicts


def parse_bibtex_file(file_path: str) -> list[dict[str, Any]]:
    """Parse a BibTeX file and extract entries into a list of dictionaries.

    Args:
        file_path (str): Path to the BibTeX file.

    Returns:
        list[dict[str, Any]]: List of dictionaries representing BibTeX entries.
    """
    with open(file_path, "r", encoding=ENCODING) as file:
        entries = []
        current_entry: Optional[dict[str, Any]] = None
        for line in file:
            line = line.strip()
            if not line or line.startswith("%"):
                # Skip empty lines and comments
                continue
            if line.startswith("@"):
                # New entry
                if current_entry:
                    entries.append(current_entry)
                parts = line.split("{")
                current_entry = {
                    COL_ENTRYTYPE: parts[0][1:].lower(),
                    COL_CITATIONKEY: parts[1][:-1],
                }
            elif line.startswith("}"):
                # End of entry
                if current_entry:
                    entries.append(current_entry)
                current_entry = None
            else:
                # Field
                parts = line.split("=")
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()[:-1].strip('{}"')
                    if current_entry:
                        if key == "author":
                            current_entry[key] = parse_author_str(value)
                        else:
                            current_entry[key] = value
        return entries

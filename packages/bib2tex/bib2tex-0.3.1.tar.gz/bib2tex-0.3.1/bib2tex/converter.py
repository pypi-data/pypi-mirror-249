import logging
import os
import re
from typing import Any, Optional

from bib2tex.config import (
    COL_CITATIONKEY,
    COL_ENTRYTYPE,
    BIBTEX_ENTRY_TYPES,
    ENCODING,
    LATEX_INDENT,
)
from bib2tex.bibtex_parser import parse_bibtex_file
from bib2tex.bibtex_filter import filter_by_key, filter_entries, sort_entries
from bib2tex.file_handler import string_to_file
from bib2tex.format_schemes import FormatSchemeManager
import bib2tex.custom_types as ct

logging.getLogger(__name__)


class NoEntryError(Exception):
    pass


def find_missing_values_in_format_string(input_string: str) -> set[str]:
    """Identify BibTeX tags lacking values within a completed format scheme.

    Based on tag in uppercase letters and wrapped in <> in a string.

    Args:
        input_string (str): Input string.

    Returns:
        set[str]: Set of BibTeX tags with missing values in the format scheme.
    """
    pattern = r"<([A-Z]+)>"
    matches = re.findall(pattern, input_string)
    return {match.lower() for match in matches}


def check_missing_values(
    input_string: str, citationkey: str, entry_type: Optional[str] = None
) -> None:
    """Log a warning if BibTeX tags within a format scheme lack values.

    Args:
        input_string (str): Format scheme containing BibTeX tags.
        citationkey (str): Citation key associated with the input.
        entry_type (str): Entry type, included in log if provided.

    Returns:
        None. Logs a warning if missing values are found.
    """
    tags = find_missing_values_in_format_string(input_string)
    msg = f"Missing {'values' if len(tags) > 1 else 'value'} in {citationkey!r}:"
    if entry_type:
        msg = msg[:-1] + f" ({entry_type}):"
    if len(tags) > 0:
        logging.warning(f"{msg} {', '.join(tags)}")


def get_latex_string(
    entries: list[dict[str, Any]],
    format_schemes: dict[str, str],
    underline: Optional[str],
    indent: int = LATEX_INDENT,
    item_options: str = "",
    itemize_options: str = "",
    type_in_warning: bool = False,
) -> str:
    """Create LaTeX itemization environment with BibTeX entries.

    Args:
        entries (list[dict[str, Any]]): List of BibTeX entries.
        format_scheme (str): LaTeX format scheme.
        underline (Optional[str]): String to underline in author names.
        indent (int, optional): Number of spaces for indentation.
        item_options (str, optional): Options for LaTeX item.
        itemize_options (str, optional): Options for LaTeX itemize.
        type_in_warning (bool): Show entry type in warning for values missing in string.

    Returns:
        str: LaTeX itemization string.
    """
    strings = []
    for entry in entries:
        format_scheme = format_schemes[entry[COL_ENTRYTYPE]]
        authors = [f"{d['name_first'][:1]}.~{d['name_last']}" for d in entry["author"]]
        if underline is not None:
            authors = [
                r"\underline{" + a + "}" if underline.lower() in a.lower() else a for a in authors
            ]
        entry["author"] = ", ".join(authors)
        string = indent * " " + "\\item" + f"{item_options} " + format_scheme
        for tag in entry:
            string = string.replace(f"<{tag.upper()}>", entry[tag])
        check_missing_values(
            string,
            entry[COL_CITATIONKEY],
            entry[COL_ENTRYTYPE] if type_in_warning else None,
        )
        strings.append(string)
    return (
        "\\begin{itemize}"
        + itemize_options
        + "\n"
        + "\n".join(strings)
        + "\n"
        + "\\end{itemize}"
    )


def to_latex(
    bibtex_path: str,
    output_dir: str,
    author: str,
    entrytypes: list[str],
    definitions: Optional[str],
    format_scheme: str = "default",
    item: str = "",
    itemize: str = "",
    highlight: bool = True,
    case_sensitive: bool = False,
    merge: bool = False,
    reverse: bool = False,
    force: bool = False,
    format_scheme_manager: FormatSchemeManager = FormatSchemeManager(),
) -> None:
    """Conversion of BibTeX entries of the specified author.

    Args:
        bibtex_path (str): Path to the BibTeX file.
        output_dir (str): Path to the output directory for LaTeX files.
        author (str): Author name for filtering entries.
        entrytypes (List[str]): Entry type(s) for filtering; declare multiple times for batch conversion.
        definitions (Optional[str]): Path to a JSON file with custom type definitions.
        format_scheme (str, optional): Scheme name for LaTeX item formatting. Defaults to "default".
        item (str, optional): Options for LaTeX item, e.g., "[--]". Defaults to "".
        itemize (str, optional): Options for LaTeX itemize, e.g., "[itemsep=3pt]". Defaults to "".
        highlight (bool, optional): Underline the author in the LaTeX item. Defaults to True.
        case_sensitive (bool, optional): Case-sensitive filtering. Defaults to False.
        merge (bool, optional): Merge individual lists into one list (batch). Defaults to False.
        reverse (bool, optional): Sort entries from old to new. Defaults to False.
        force (bool, optional): Perform the conversion without confirmations. Defaults to False.
        format_scheme_manager (FormatSchemeManager, optional): Format scheme manager instance.

    Raises:
        NoEntryError: Raised when no entry is found for the specified author.
    """
    result_entries: dict[str, Any] = {}

    # load data from BibTeX file
    bibtex_filename = os.path.basename(bibtex_path)
    entries = parse_bibtex_file(bibtex_path)
    logging.info(f"Loaded {len(entries)} entries from BibTeX file {bibtex_filename!r}.")

    # initialise format scheme manager and register custom types
    if definitions:
        ct.register_custom_types(
            file_path=definitions, format_scheme_manager=format_scheme_manager
        )

    # filter entries for author
    author_entries = filter_entries(
        entries, author, None, case_sensitive=case_sensitive, reverse=reverse
    )

    # filter entries for types
    for key in entrytypes:
        if key is None:
            filtered_entries = author_entries
        elif key in BIBTEX_ENTRY_TYPES:
            logging.debug(f"Converting BibTeX entry type {key!r}")
            filtered_entries = filter_by_key(author_entries, COL_ENTRYTYPE, key)
        elif key in ct.get_custom_type_names():
            logging.debug(f"Converting custom entry type {key!r}")
            filtered_entries = ct.get_entries_for_custom_type(author_entries, key)
        else:
            logging.warning(f"Invalid entry type: {key!r}. Skipping!")
            continue

        entry_count = len(filtered_entries)
        if entry_count == 0 and key is not None:
            logging.warning(
                f"No {key!r} entry found for {author!r} in {bibtex_filename!r}."
            )
            continue

        logging.info(
            f"Found {entry_count} {key!r}{' entries' if entry_count !=1 else ' entry'} for {author!r} in {bibtex_filename!r}."
        )

        # append entries to result dictionary
        result_entries[key] = filtered_entries

    if len(filtered_entries) == 0:
        raise NoEntryError(f"No entry found for {author!r} in {bibtex_filename!r}.")

    # Map output filenames to result entries
    to_write: dict[str, list[dict[str, Any]]] = {}
    if merge:
        merged_entries = [e for entries in result_entries.values() for e in entries]
        types_str = (
            "_" + "-".join(list(result_entries.keys())) if key is not None else ""
        )
        filename = f"{author.lower()}{types_str}.tex"
        to_write = {filename: sort_entries(merged_entries, reverse=not reverse)}
    else:
        if key is not None:
            to_write = {
                f"{author.lower()}_{k}.tex": v for k, v in result_entries.items()
            }
        else:
            to_write[f"{author.lower()}.tex"] = list(result_entries.values())[0]

    # retrieve format scheme dictionary (type/scheme mapping)
    fs_dict = format_scheme_manager.get_format_schemes(format_scheme)

    # define underline string if desired
    underline = author if highlight else None

    # Include type in missing value warning if batch mode
    type_in_warning = False
    if len(to_write) > 1 or merge or entrytypes == (None,):
        type_in_warning = True

    # create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.debug(f"Output directory {output_dir!r} created.")

    for filename, entries in to_write.items():
        # convert entries to LaTeX list
        latex_string = get_latex_string(
            entries,
            underline=underline,
            item_options=item,
            itemize_options=itemize,
            format_schemes=fs_dict,
            type_in_warning=type_in_warning,
        )
        logging.debug(f"LaTeX {key!r} list created for {author!r}.")

        # write Latex list to file
        out_path = os.path.join(output_dir, filename)
        if os.path.isfile(out_path) and not force:
            user_input = input(f"LaTeX file {out_path!r} exists, overwrite it? [y/N]: ")
            if not user_input.lower() == "y":
                continue
        string_to_file(out_path, latex_string)
        logging.info(f"LaTeX string written to {out_path!r}.")


import logging
import re
from typing import Any, Optional

from bib2tex.config import COL_CITATIONKEY, COL_ENTRYTYPE, ENCODING, LATEX_INDENT


def find_missing_values(input_string: str) -> set[str]:
    """Identify BibTeX tags lacking values within a completed format scheme.

    Based on tag in uppercase letters and wrapped in <> in a string.

    Args:
        input_string (str): Input string.

    Returns:
        set[str]: Set of BibTeX tags with missing values in the format scheme.
    """
    pattern = r'<([A-Z]+)>'
    matches = re.findall(pattern, input_string)
    return {match.lower() for match in matches}


def check_missing_values(input_string: str, citationkey: str) -> None:
    """Log a warning if BibTeX tags within a format scheme lack values.

    Args:
        input_string (str): Format scheme containing BibTeX tags.
        citationkey (str): Citation key associated with the input.

    Returns:
        None. Logs a warning if missing values are found.
    """
    tags = find_missing_values(input_string)
    if len(tags) > 0:
        logging.warning(
                f"Missing {'values' if len(tags) > 1 else 'value'} in {citationkey!r}: {', '.join(tags)}"
        )


def to_latex(
    entries: list[dict[str, Any]],
    format_schemes: dict[str,str],
    underline: Optional[str],
    indent: int = LATEX_INDENT,
    item_options: str = "",
    itemize_options: str = "",
) -> str:
    """Convert BibTeX entries to LaTeX itemization.

    Args:
        entries (list[dict[str, Any]]): List of BibTeX entries.
        format_scheme (str): LaTeX format scheme.
        underline (Optional[str]): String to underline in author names.
        indent (int, optional): Number of spaces for indentation.
        item_options (str, optional): Options for LaTeX item.
        itemize_options (str, optional): Options for LaTeX itemize.

    Returns:
        str: LaTeX itemization string.
    """
    strings = []
    for entry in entries:
        format_scheme = format_schemes[entry[COL_ENTRYTYPE]]
        authors = [f"{d['name_first'][:1]}.~{d['name_last']}" for d in entry["author"]]
        if underline is not None:
            authors = [
                r"\underline{" + a + "}" if underline in a else a for a in authors
            ]
        entry["author"] = ", ".join(authors)
        string = indent * " " + "\\item" + f"{item_options} " + format_scheme
        for tag in entry:
            string = string.replace(f"<{tag.upper()}>", entry[tag])
        check_missing_values(string, entry[COL_CITATIONKEY])
        strings.append(string)
    return (
        "\\begin{itemize}"
        + itemize_options
        + "\n"
        + "\n".join(strings)
        + "\n\\end{itemize}"
    )


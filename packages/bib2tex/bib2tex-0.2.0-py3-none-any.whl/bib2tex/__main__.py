"""
This module provides a command-line interface (CLI) for filtering and
converting BibTeX entries to a LaTeX list. It uses the click library for
command-line argument parsing.
"""

import logging
import os
import sys
from typing import Optional

import click

from bib2tex import custom_types as ct
from bib2tex.bibtex_filter import filter_entries
from bib2tex.bibtex_parser import parse_bibtex_file
from bib2tex.config import BIBTEX_ENTRY_TYPES, DEFAULT_BIB_PATH
from bib2tex.converter import to_latex
from bib2tex.file_handler import string_to_file
from bib2tex.format_schemes import FormatSchemeManager

class CustomFormatter(logging.Formatter):
    """A custom logging formatter.

    It includes the level name for WARNING, ERROR, and CRITICAL levels, and
    excludes it for other levels.
    """
    def format(self, record):
        if record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL):
            self._style._fmt = "%(levelname)s: %(message)s"
        else:
            self._style._fmt = "%(message)s"
        return super().format(record)

def setup_logger(verbose: bool):
    """Set up logging configuration based on the verbosity level.

    Args:
        verbose (bool): If True, set logging level to INFO; otherwise, set it to ERROR.
    """
    log_level = logging.INFO if verbose else logging.ERROR
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    console_handler = logging.StreamHandler()
    formatter = CustomFormatter()
    console_handler.setFormatter(formatter)
    # Clear existing handlers to avoid duplicates
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(console_handler)

def main(
    bibtex_path: str,
    latex_path: str,
    author: str,
    definitions: Optional[str],
    entrytype: Optional[str],
    format_scheme: str = "default",
    item: str = "",
    itemize: str = "",
    highlight: bool = True,
    reverse: bool = False,
    verbose: bool = True,
) -> None:
    """Convert BibTeX entries of the specified author (and entrytype) into a LaTeX item environment.

    This function serves as the entry point for the CLI.

    Args:
        bibtex_path (str): Path to the BibTeX file.
        latex_path (str): Path to the LaTeX file.
        author (str): Author name for filtering entries.
        definitions (str): Path to a JSON file with custom type definitions.
        entrytype (Optional[str]): BibTeX entry type for filtering.
        format_scheme (str): Format scheme name for LaTeX item.
        item (str): Options for LaTeX item, e.g., '[--]'.
        itemize (str): Options for LaTeX itemize.
        highlight (bool): If True, underline the author in LaTeX.
        reverse (bool): If True, sort entries from old to new.
        verbose (bool): If True, print verbose output.
    """
    setup_logger(verbose=verbose)

    # load data from BibTeX file
    bibtex_filename = os.path.basename(bibtex_path)
    entries = parse_bibtex_file(bibtex_path)
    logging.info(f"Loaded {len(entries)} entries from BibTeX file {bibtex_filename!r}.")

    # initialise format scheme manager and register custom types
    fsm = FormatSchemeManager()
    if definitions:
        ct.register_custom_types(file_path=definitions, fsm=fsm)

    # filter entries for author (and type)
    if entrytype in BIBTEX_ENTRY_TYPES or entrytype is None:
        filtered_entries = filter_entries(entries, author, entrytype, reverse=reverse)
    elif entrytype in ct.get_custom_type_names():
        a_entries = filter_entries(entries, author, None, reverse=reverse)
        filtered_entries = ct.get_entries_for_custom_type(a_entries, entrytype)
    else:
        logging.warning(f"{entrytype!r} is not a valid BibTeX or custom type. Aborting!")
        sys.exit()

    if len(filtered_entries) == 0:
        logging.info(
            f"Found no{' ' + entrytype if entrytype is not None else ''} entries for {author!r}. Aborting!"
        )
        sys.exit()
    logging.info(
        f"Converting {len(filtered_entries)}{' ' + entrytype if entrytype is not None else ''} entries for {author!r} into LaTeX string..."
    )

    # retrieve format scheme dictionary (type/scheme mapping)
    format_schemes = fsm.get_format_schemes(format_scheme)

    # define underline string if desired
    underline = author if highlight else None

    # create LaTeX string and write to output file
    latex_string = to_latex(
        filtered_entries,
        underline=underline,
        item_options=item,
        itemize_options=itemize,
        format_schemes=format_schemes,
    )
    string_to_file(latex_path, latex_string)
    logging.info(f"LaTeX string written to {latex_path!r}.")


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    epilog="by Cs137, 2023 - development on Codeberg: https://codeberg.org/Cs137/bib2tex",
)
@click.option(
    "-i",
    "--bibtex-path",
    default=DEFAULT_BIB_PATH,
    show_default=True,
    required=True,
    type=click.Path(exists=True),
    help="(input) Path to the BibTeX file.",
    # prompt="Enter the path to the BibTeX file (input)",
)
@click.option(
    "-o",
    "--latex-path",
    required=True,
    type=click.Path(),
    help="(output) Path to the LaTeX file",
    prompt="Enter the path to the LaTeX file (output)",
)
@click.option(
    "-a",
    "--author",
    required=True,
    help="Author name for filtering entries.",
    prompt="Enter the author name for filtering BibTeX entries",
)
@click.option(
    "-d",
    "--definitions",
    type=click.Path(exists=True),
    help="Path to a JSON file with custom type definitions.",
)
@click.option("-e", "--entrytype", help="BibTeX entry type for filtering.")
@click.option("-f", "--format-scheme", default='default', help="Format scheme name for LaTeX item.")
@click.option("-r", "--reverse", is_flag=True, help="Sort entries from old to new.")
@click.option("-u", "--underline", "highlight", is_flag=True, help="Underline the author in LaTeX.")
@click.option("-v", "--verbose", is_flag=True, help="Print verbose output.")
@click.option("--item", default="", help='Options for LaTeX item, e.g. "[--]".')
@click.option("--itemize", default="", help='Options for LaTeX itemze, e.g. "[itemsep=3pt]".')
def cli(**kwargs) -> None:
    """Filter BibTeX entries by author and type, converting the subset into a LaTeX
    list. The defined author can be highlighted, and entries are sorted from newest
    to oldest by default.
    \f
    This function is a wrapper that defines the options and invokes the main function.

    Args:
        **kwargs: Keyword arguments corresponding to CLI options.
    """
    main(**kwargs)


if __name__ == "__main__":
    cli()


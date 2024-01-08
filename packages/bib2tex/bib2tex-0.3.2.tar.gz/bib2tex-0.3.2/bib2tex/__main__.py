"""
This module provides a command for the CLI for filtering and converting
BibTeX entries into a LaTeX list.
"""

import logging
import sys
from typing import Any, Optional

import click

from bib2tex import package_name, version
from bib2tex import custom_types as ct
from bib2tex.config import (
    BIBTEX_ENTRY_TYPES,
    CLI_EPILOG,
    COL_ENTRYTYPE,
    DEFAULT_BIB_PATH,
)
from bib2tex.converter import to_latex, NoEntryError


class CustomFormatter(logging.Formatter):
    """A custom logging formatter.

    It includes the level name for WARNING, ERROR, and CRITICAL levels, and
    excludes it for other levels.
    """

    def __init__(self):
        fmt = "%(levelname)s: %(message)s"
        super().__init__(fmt)

    def format(self, record):
        if record.levelno not in (logging.WARNING, logging.ERROR, logging.CRITICAL):
            self._fmt = "%(message)s"
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


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    epilog=CLI_EPILOG,
)
@click.option(
    "-i",
    "--bibtex-path",
    default=DEFAULT_BIB_PATH,
    show_default=True,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="(input) Path to the BibTeX file.",
    # prompt="Enter the path to the BibTeX file (input)",
)
@click.option(
    "-o",
    "--output-dir",
    default=".",
    show_default=True,
    required=True,
    type=click.Path(file_okay=False),
    help="Path to output directory for LaTeX files.",
    # prompt="Enter the path to the output directory",
)
@click.option(
    "-a",
    "--author",
    required=True,
    help="Author name for filtering entries.",
    prompt="Enter the author name for filtering BibTeX entries",
)
@click.option("-c", "--case-sensitive", is_flag=True, help="Case sensitive filtering.")
@click.option(
    "-d",
    "--definitions",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a JSON file with custom type definitions.",
)
@click.option(
    "-e",
    "--entry-type",
    "entrytypes",
    multiple=True,
    default=[None],
    help="Specify entry type for filtering; declare multiple times for batch conversion.",
    # prompt="Enter the type(s) for filtering BibTeX entries",
)
@click.option(
    "-f", "--force", is_flag=True, help="Perform the conversion without confirmations."
)
@click.option(
    "-m", "--merge", is_flag=True, help="Merge individual lists into one list (batch)."
)
@click.option("-r", "--reverse", is_flag=True, help="Sort entries from old to new.")
@click.option(
    "-s",
    "--format-scheme",
    default="default",
    help="Scheme name for LaTeX item formatting.",
)
@click.option(
    "-u",
    "--underline",
    "highlight",
    is_flag=True,
    help="Underline the author in the LaTeX item.",
)
@click.option("-v", "--verbose", is_flag=True, help="Print verbose output.")
@click.option("--item", default="", help='Options for LaTeX item, e.g. "[--]".')
@click.option(
    "--itemize", default="", help='Options for LaTeX itemze, e.g. "[itemsep=3pt]".'
)
@click.version_option(version=version)
def cli(**kwargs) -> None:
    """bib2tex - A command line utility to generate LaTeX lists from BibTeX data.

    Sorted lists are generated based on an author's name and entry types (optional).
    They are either merged into a LaTeX item environment and written into a file,
    or stored in individual files as LaTeX item environment.

    The files are written to the output directory and are named based on the filter
    options. If no entry type is declared, the filename is 'author.tex', while it
    is 'author_entrytype.tex' if you filter for one entry type, and
    'author_entrytype1-entrytype2-entrytypeN.tex' if multiple entry types are declared.
    \f
    This function is a wrapper that defines the options and invokes the to_latex converter.

    Args:
        **kwargs: Keyword arguments corresponding to CLI options.
    """
    verbose = kwargs.pop("verbose")
    setup_logger(verbose=verbose)
    logging.info(f"Running {package_name} v{version}")

    # Start conversion
    try:
        to_latex(**kwargs)
    except NoEntryError as e:
        logging.warning(e)

    # Exit script
    logging.info(f"Completed {package_name} execution.")
    sys.exit()


if __name__ == "__main__":
    cli()


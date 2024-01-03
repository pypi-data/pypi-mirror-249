import os

# Path to .bib file used as default in the CLI
# Default is the environment variable "BIB"
DEFAULT_BIB_PATH = os.environ.get("BIB")

# Encoding used to read from BibTeX and to latex files
ENCODING = "utf-8"

# Key names for columns in addition to found BibTeX tags
COL_ENTRYTYPE = "entrytype"
COL_CITATIONKEY = "citationkey"
COL_NAME_FULL = "name"
COL_NAME_FIRST = "name_first"
COL_NAME_LAST = "name_last"

# Format scheme mappings for LaTeX items
FORMAT_SCHEMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "format_schemes/")

# Indent for items within the itemize environment
LATEX_INDENT = 2

# List of BibTeX Entry Types
BIBTEX_ENTRY_TYPES = [
    "article",
    "book",
    "booklet",
    "conference",
    "inbook",
    "incollection",
    "inproceedings",
    "manual",
    "mastersthesis",
    "misc",
    "phdthesis",
    "proceedings",
    "techreport",
    "unpublished"
]

# Keys required in definitions of custom entry types
CT_KEY_BIBTEXTYPE = 'bibtex_type'
CT_KEY_FORMATSCHEMES = 'format_schemes'
CT_KEY_SEARCHSTRING = 'search_strings'


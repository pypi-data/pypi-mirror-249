"""Helper functions to handle file related tasks."""

import json
from typing import Any, Union

from bib2tex.config import ENCODING


def read_json_file(
    file_path: str, encoding: str = ENCODING
) -> Union[list[Any], dict[str, Any]]:
    """Read data from a JSON file and return as dict of strings.

    Args:
        file_path (str): Path to the file.
        encoding (str, optional): Encoding of the file.
    """
    with open(file_path, "r", encoding=encoding) as file:
        data = json.load(file)
    return data


def string_to_file(file_path: str, string: str, encoding: str = ENCODING) -> None:
    """Write a string to a file.

    Args:
        file_path (str): Path to the file.
        string (str): String to write to the file.
        encoding (str, optional): Encoding of the file.
    """
    with open(file_path, "w", encoding=encoding) as file:
        file.write(string)

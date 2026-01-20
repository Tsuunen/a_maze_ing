from pathlib import Path
import os
from typing import Iterator
from pydantic import ValidationError


class Parser:
    """Base parser class"""

    def __init__(self, file_path: str) -> None:
        if Path(file_path).is_file() and os.access(file_path, os.R_OK):
            self.file_path = file_path
        else:
            raise FileNotFoundError(
                f"{file_path} does not exist or is not readable")

    def iter_lines(self) -> Iterator[str]:
        """"Yield file line one by one"""
        with open(self.file_path, "r") as file:
            for line in file:
                yield line.rstrip("\n")

    def format_validation_error(self, e: ValidationError) -> str:
        """Format ValidationError for them to be more clear

        e -- The ValidationError to format
        """
        lines = []
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            msg = err["msg"]
            lines.append(f"- {field}: {msg}")
        return ("Invalid configuration:\n" + "\n".join(lines))

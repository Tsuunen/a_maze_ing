from pathlib import Path
import os
from typing import Tuple, Iterator
from pydantic import (BaseModel, Field, field_validator, FieldValidationInfo,
                      ValidationError, model_validator)


class Config(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Tuple[int, int] = Field(min_length=2, max_length=2)
    exit: Tuple[int, int] = Field(min_length=2, max_length=2)
    output_file: str = Field()
    perfect: bool = Field()

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_2tuple(cls, raw: str,
                     info: FieldValidationInfo) -> Tuple[int, int]:
        opt = raw.split(",")
        opt = [o.strip() for o in opt]
        if (len(opt) != 2):
            raise ValueError(f"{info.field_name} is not a valid coord input")
        try:
            return ((int(opt[0]), int(opt[1])))
        except ValueError:
            raise ValueError(f"{info.field_name} must contain integers")

    @model_validator(mode="after")
    def check_valid_coords(self):
        if (self.entry == self.exit):
            raise ValueError("entry and exit must not overlap")
        if (self.entry[0] < 0 or self.entry[0] > self.width or
            self.entry[1] < 0 or self.entry[1] > self.height or
            self.exit[0] < 0 or self.exit[0] > self.width or
                self.exit[1] < 0 or self.exit[1] > self.height):
            raise ValueError("coords are out of bound")
        if (self.entry[0] not in [0, self.width] and
                self.entry[1] not in [0, self.height]):
            raise ValueError("entry is not on the maze border")
        if (self.exit[0] not in [0, self.width] and
                self.exit[1] not in [0, self.height]):
            raise ValueError("exit is not on the maze border")
        return (self)


class ConfigParser:
    def __init__(self, file_path: str):
        if Path(file_path).is_file() and os.access(file_path, os.R_OK):
            self.file_path = file_path
        else:
            raise FileNotFoundError(
                f"{file_path} does not exist or is not readable")

    def iter_lines(self) -> Iterator[str]:
        with open(self.file_path, "r") as file:
            for line in file:
                yield line.rstrip("\n").strip()

    def format_validation_error(self, e: ValidationError) -> str:
        lines = []
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            msg = err["msg"]
            lines.append(f"- {field}: {msg}")
        return "Invalid configuration:\n" + "\n".join(lines)

    def extract(self) -> Config:
        config = {}
        for line in self.iter_lines():
            if (not len(line) or line[0] == "#"):
                continue
            opt = line.split("=")
            if (len(opt) != 2):
                continue
            config[opt[0].lower()] = opt[1]
        try:
            return (Config.model_validate(config))
        except ValidationError as e:
            print(self.format_validation_error(e))

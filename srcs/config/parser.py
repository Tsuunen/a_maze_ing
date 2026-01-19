from typing import Tuple
from typing_extensions import Self
from pydantic import (BaseModel, Field, field_validator, ValidationInfo,
                      ValidationError, model_validator)
from ..parser import Parser


class Config(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Tuple[int, int] = Field(min_length=2, max_length=2)
    exit: Tuple[int, int] = Field(min_length=2, max_length=2)
    output_file: str = Field()
    perfect: bool = Field()
    seed: int | None = Field(default=None)
    shape: str = Field(default="rectangle")

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_2tuple(cls, raw: str,
                     info: ValidationInfo) -> Tuple[int, int]:
        if (isinstance(raw, tuple)):
            return (raw)
        opt = raw.split(",")
        opt = [o.strip() for o in opt]
        if (len(opt) != 2):
            raise ValueError(f"{info.field_name} is not a valid coord input")
        try:
            return ((int(opt[0]), int(opt[1])))
        except ValueError:
            raise ValueError(f"{info.field_name} must contain integers")

    @model_validator(mode="after")
    def check_valid_coords(self) -> Self:
        if (self.entry == self.exit):
            raise ValueError("entry and exit must not overlap")
        if (self.entry[0] < 0 or self.entry[0] >= self.width or
            self.entry[1] < 0 or self.entry[1] >= self.height or
            self.exit[0] < 0 or self.exit[0] >= self.width or
                self.exit[1] < 0 or self.exit[1] >= self.height):
            raise ValueError("coords are out of bound")
        if (self.shape not in ["rectangle", "square", "circle", "donut",
                               "diamond", "elipse"]):
            raise ValueError("Shape not known")
        return (self)


class ConfigParser(Parser):
    def extract(self) -> Config | None:
        config = {}
        for line in self.iter_lines():
            line = line.strip()
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
            return (None)

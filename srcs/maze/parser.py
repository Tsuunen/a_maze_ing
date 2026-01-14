from pydantic import (BaseModel, Field, field_validator,
                      FieldValidationInfo, ValidationError, model_validator)
from ..parser import Parser
from typing import Tuple


class Maze(BaseModel):
    maze: str = Field()
    entry: Tuple[int, int] = Field(min_length=2, max_length=2)
    exit: Tuple[int, int] = Field(min_length=2, max_length=2)
    path: str = Field()
    nbr_cols: int = Field(ge=1)
    nbr_rows: int = Field(ge=1)

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
        if (self.entry[0] < 0 or self.entry[0] > self.nbr_cols or
            self.entry[1] < 0 or self.entry[1] > self.nbr_rows or
            self.exit[0] < 0 or self.exit[0] > self.nbr_cols or
                self.exit[1] < 0 or self.exit[1] > self.nbr_rows):
            raise ValueError("coords are out of bound")
        for c in self.maze:
            if (c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                          "A", "B", "C", "D", "E", "F", "\n", " "]):
                raise ValueError(f"{c} is an invalid maze character")
        for c in self.path:
            if (c not in ["N", "S", "E", "W"]):
                raise ValueError(f"{c} is an invalid path character")
        self.maze = self.maze[:-1]
        for line in self.maze.split("\n"):
            if (len(line) != self.nbr_cols):
                raise ValueError("Maze line are not the same size")
        return (self)


class MazeParser(Parser):
    def extract(self):
        nbr_rows = 0
        maze = ""
        is_maze = True
        count = 0
        exit = ""
        entry = ""
        path = ""
        for line in self.iter_lines():
            if (not line):
                is_maze = False
                continue
            if (is_maze):
                nbr_rows += 1
                nbr_cols = len(line)
                maze += line + "\n"
            else:
                if (count == 0):
                    entry = line
                elif (count == 1):
                    exit = line
                else:
                    path = line
                count += 1

        try:
            return (Maze(maze=maze,
                         nbr_cols=nbr_cols,
                         nbr_rows=nbr_rows,
                         entry=entry,
                         exit=exit,
                         path=path))
        except ValidationError as e:
            print(self.format_validation_error(e))

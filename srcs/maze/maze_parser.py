from ..parser import Parser
from pydantic import ValidationError
from ..mazegen.maze_gen import Maze


class MazeParser(Parser):
    """Class to parse a maze file

    Args:
    file_path: The path of the config file
    """

    def extract(self) -> Maze | None:
        """Extract the maze from the maze file

        Returns:
        A Maze object filled

        Raises:
        A formatted error message
        """
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
            return Maze.model_validate({
                "maze": maze,
                "nbr_cols": nbr_cols,
                "nbr_rows": nbr_rows,
                "entry": entry,
                "exit": exit,
                "path": path,
            })
        except ValidationError as e:
            print(self.format_validation_error(e))
            return None

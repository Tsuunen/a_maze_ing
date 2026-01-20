import random
from math import sqrt
from ..config.parser import Config
from typing import Tuple
from typing_extensions import Self
from pydantic import (BaseModel, Field, field_validator,
                      ValidationInfo, model_validator)


class Maze(BaseModel):
    """Maze object"""
    maze: str = Field()
    entry: Tuple[int, int] = Field(min_length=2, max_length=2)
    exit: Tuple[int, int] = Field(min_length=2, max_length=2)
    path: str = Field()
    nbr_cols: int = Field(ge=1)
    nbr_rows: int = Field(ge=1)
    seed: int | None = Field(default=None)

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_2tuple(cls, raw: str,
                     info: ValidationInfo) -> Tuple[int, int]:
        """Parse entry and exit fields before pydantic validation

        Args:
        cls: The Config class itself
        raw: The raw entry or exit value
        info: Field information

        Returns:
        The right couple of coordinates

        Raises:
        A descriptive ValueError
        """
        if (isinstance(raw, tuple)):
            if (len(raw) != 2):
                raise ValueError(
                    f"{info.field_name} is not a valid coord input")
            try:
                return (int(raw[0]), int(raw[1]))
            except ValueError:
                raise ValueError("The tuple must contain int values")
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
        """Check after the Pydantic validation if the info are coherent

        Returns:
        The instance itself

        Raises:
        A descriptive ValueError
        """
        if (self.entry == self.exit):
            raise ValueError("entry and exit must not overlap")
        if (self.entry[0] < 0 or self.entry[0] >= self.nbr_cols or
            self.entry[1] < 0 or self.entry[1] >= self.nbr_rows or
            self.exit[0] < 0 or self.exit[0] >= self.nbr_cols or
                self.exit[1] < 0 or self.exit[1] >= self.nbr_rows):
            raise ValueError("coords are out of bound")
        for c in self.maze:
            if (c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                          "A", "B", "C", "D", "E", "F", "\n", " "]):
                raise ValueError(f"{c} is an invalid maze character")
        for c in self.path:
            if (c not in ["N", "S", "E", "W"]):
                raise ValueError(f"{c} is an invalid path character")
        self.maze = self.maze.rstrip("\n")
        for line in self.maze.split("\n"):
            if (len(line) != self.nbr_cols):
                raise ValueError("Maze line are not the same size")
        return (self)


class MazeGen:
    """
    The MazeGen obj aims to generate mazes using the dfs algorithm
    The int func takes a Config Obj and can export the Maze as a file or
    a Maze obj
    """

    def __init__(self, conf: Config):
        self.width = conf.width
        self.height = conf.height
        self.entry = conf.entry
        self.exit = conf.exit
        self.output_file = conf.output_file
        self.is_perfect = conf.perfect
        if (conf.seed):
            self.seed = conf.seed
        else:
            self.seed = random.randint(0, 2**32 - 1)
        random.seed(self.seed)
        self.visited: list[list[int]]
        self.shape = conf.shape
        self.lst_repr = [[15 for i in range(self.width)]
                         for j in range(self.height)]

    def disalign(self) -> None:
        """
        disalign entry and exit if they are on the same cell
        """
        direction: int = self.neighbors(self.entry)[0]
        match direction:
            case 0:
                self.exit = (self.entry[0], self.entry[1] - 1)
            case 1:
                self.exit = (self.entry[0] + 1, self.entry[1])
            case 2:
                self.exit = (self.entry[0], self.entry[1] + 1)
            case 3:
                self.exit = (self.entry[0] - 1, self.entry[1])

        print("entry and exit have the same projection on the shape, \
exit has been moved")

    def project_in(self) -> None:
        """
        force entry and exit inside the maze in case of special shape
        """
        while self.lst_repr[self.entry[1]][self.entry[0]] == -1:
            if self.entry[0] < self.width // 2:
                self.entry = (self.entry[0] + 1, self.entry[1])
            else:
                self.entry = (self.entry[0] - 1, self.entry[1])
            if self.lst_repr[self.entry[1]][self.entry[0]] != -1:
                continue
            if self.entry[1] < self.height // 2:
                self.entry = (self.entry[0], self.entry[1] + 1)
            else:
                self.entry = (self.entry[0], self.entry[1] - 1)

        while self.lst_repr[self.exit[1]][self.exit[0]] == -1:
            if self.exit[0] < self.width // 2:
                self.exit = (self.exit[0] + 1, self.exit[1])
            else:
                self.exit = (self.exit[0] - 1, self.exit[1])
            if self.lst_repr[self.exit[1]][self.exit[0]] != -1:
                continue
            if self.exit[1] < self.height // 2:
                self.exit = (self.exit[0], self.exit[1] + 1)
            else:
                self.exit = (self.exit[0], self.exit[1] - 1)

        if self.entry == self.exit:
            self.disalign()

    def project_out(self) -> None:
        """
        force entry and exit inside the maze in case of donut
        """
        while self.lst_repr[self.entry[1]][self.entry[0]] == -1:
            if self.entry[0] > self.width // 2:
                self.entry = (self.entry[0] + 1, self.entry[1])
            else:
                self.entry = (self.entry[0] - 1, self.entry[1])
            if self.lst_repr[self.entry[1]][self.entry[0]] != -1:
                continue
            if self.entry[1] > self.height // 2:
                self.entry = (self.entry[0], self.entry[1] + 1)
            else:
                self.entry = (self.entry[0], self.entry[1] - 1)

        while self.lst_repr[self.exit[1]][self.exit[0]] == -1:
            if self.exit[0] > self.width // 2:
                self.exit = (self.exit[0] + 1, self.exit[1])
            else:
                self.exit = (self.exit[0] - 1, self.exit[1])
            if self.lst_repr[self.exit[1]][self.exit[0]] != -1:
                continue
            if self.exit[1] > self.height // 2:
                self.exit = (self.exit[0], self.exit[1] + 1)
            else:
                self.exit = (self.exit[0], self.exit[1] - 1)

        if self.entry == self.exit:
            self.disalign()

    def project_in_square(self, size: int) -> None:
        self.entry = (min(self.entry[0], size - 1),
                      min(self.entry[1], size - 1))
        self.exit = (min(self.exit[0], size - 1), min(self.exit[1], size - 1))
        if self.entry == self.exit:
            self.disalign()
        print("entry or exit was outside the maze square, they have been moved\
 in")

    def shape_stamp(self) -> None:
        """
        makes the maze looks lkie certain shape:
        rectangle
        square
        diamond
        circle
        donut
        ellipse
        """
        self.visited = [[0 for i in range(self.width)]
                        for j in range(self.height)]
        center: tuple[int, int]
        if self.shape == "rectangle":
            return

        if self.shape in ["square", "circle", "donut", "diamond"]:
            size: int = min(self.height, self.width)
            if self.entry[0] >= size or self.entry[1] >= size or \
               self.exit[0] >= size or self.exit[1] >= size:
                self.project_in_square(size)

            self.width, self.height = size, size
            self.lst_repr = [[15 for i in range(self.width)]
                             for j in range(self.height)]
            self.visited = [[0 for i in range(self.width)]
                            for j in range(self.height)]

        if self.shape in ["circle", "donut"]:
            center = (size // 2, size // 2)
            for line in range(size):
                for col in range(size):
                    if sqrt((center[0] - line)**2 + (center[1] - col)**2) \
                            > size // 2:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_in()

        if self.shape == "donut":
            center = (size // 2, size // 2)
            for line in range(size):
                for col in range(size):
                    if sqrt((center[0] - line)**2 + (center[1] - col)**2) \
                            < size // 5:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_out()

        if self.shape == "diamond":
            center = (size // 2, size // 2)
            for line in range(size):
                for col in range(size):
                    if AStar.dist(center, (col, line)) > size // 2:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_in()

        if self.shape == "ellipse":
            center = (self.width // 2, self.height // 2)
            for line in range(self.height):
                for col in range(self.width):
                    if (col - center[0]) ** 2 / center[0] ** 2 + \
                       (line - center[1]) ** 2 / center[1] ** 2 > 1:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_in()

    def ft_stamp(self, error: bool) -> None:
        """
        put the '42 stamp' on the maze if possible
        """
        if self.width < 9 or self.height < 7 or \
           (self.shape in ["circle", "ellipse", "diamond", "donut"] and
               (self.height < 14 or self.width < 14)):
            if error:
                print("42 logo cannot be represented(maze too small)")
            return
        center: tuple[int, int] = (self.width // 2, self.height // 2)
        stamp: list[tuple[int, int]] = [
            (center[0] - 3, center[1] - 2),
            (center[0] - 3, center[1] - 1),
            (center[0] - 3, center[1]),
            (center[0] - 2, center[1]),
            (center[0] - 1, center[1]),
            (center[0] - 1, center[1] + 1),
            (center[0] - 1, center[1] + 2),
            (center[0] + 1, center[1] - 2),
            (center[0] + 2, center[1] - 2),
            (center[0] + 3, center[1] - 2),
            (center[0] + 3, center[1] - 1),
            (center[0] + 1, center[1]),
            (center[0] + 2, center[1]),
            (center[0] + 3, center[1]),
            (center[0] + 1, center[1] + 1),
            (center[0] + 1, center[1] + 2),
            (center[0] + 2, center[1] + 2),
            (center[0] + 3, center[1] + 2),
        ]
        for coord in stamp:
            if coord == self.entry or coord == self.exit:
                if error:
                    print("42 logo cannot be represented(entry or exit present\
 in the logo)")
                return
        for coord in stamp:
            self.visited[coord[1]][coord[0]] = 1
            self.lst_repr[coord[1]][coord[0]] = 15

    @staticmethod
    def hexa(x: int) -> str:
        """
        takes an integer and return it's hexadecimal representation
        """
        hexa = ["0", "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "A", "B", "C", "D", "E", "F"]
        try:
            if x == -1:
                return " "
            return hexa[x]
        except Exception:
            return " "

    def str_repr(self, error: bool) -> str:
        """
        returns a representation of the maze and it s solution as a string
        """
        repr = ""
        for i in self.lst_repr:
            for j in i:
                repr += self.hexa(j)
            repr += "\n"
        repr += f"\n{self.entry[0]},{self.entry[1]}\n\
{self.exit[0]},{self.exit[1]}\n"
        try:
            repr += self.solve()
        except (TypeError):
            if error:
                print("Maze with no solution cannot be represented")
            repr += " "
        return repr

    def export_maze_file(self) -> None:
        """
        export the list representation of the maze in a .txt file
        """
        with open(self.output_file, "w") as f:
            f.write(self.str_repr(True))

    def export_maze_obj(self) -> Maze:
        """
        export the maze as an object for further treatment
        """
        repr = self.str_repr(False)
        return Maze(
            maze=repr[:(self.width + 1) * self.height],
            entry=self.entry,
            exit=self.exit,
            path=repr.splitlines()[self.height + 3],
            nbr_cols=self.width,
            nbr_rows=self.height,
            seed=self.seed
        )

    def solve(self) -> str:
        """
        solve the maze
        return a string representing mooves necessary to solve it
        """
        solver: AStar = AStar(self)
        solution: str | None = solver.solve(self)
        if not solution:
            raise Exception("an error occured, the maze has no solution")
        return solution

    def dig_wall(self, pos: tuple[int, int], direction: int) -> None:
        """
        given a pos and a dirrection,
        removes the wall between a position and the destination
        """
        if direction == 0 and self.lst_repr[pos[1]][pos[0]] & 1:
            self.lst_repr[pos[1]][pos[0]] -= 1
            self.lst_repr[pos[1] - 1][pos[0]] -= 4
        elif direction == 1 and self.lst_repr[pos[1]][pos[0]] & 2:
            self.lst_repr[pos[1]][pos[0]] -= 2
            self.lst_repr[pos[1]][pos[0] + 1] -= 8
        elif direction == 2 and self.lst_repr[pos[1]][pos[0]] & 4:
            self.lst_repr[pos[1]][pos[0]] -= 4
            self.lst_repr[pos[1] + 1][pos[0]] -= 1
        elif direction == 3 and self.lst_repr[pos[1]][pos[0]] & 8:
            self.lst_repr[pos[1]][pos[0]] -= 8
            self.lst_repr[pos[1]][pos[0] - 1] -= 2

    def neighbors(self, pos: tuple[int, int]) -> list[int]:
        """
        takes a pos in the currently generating maze (pos[x, y])
        return the list of unexplored neighbors
        """
        output = []
        if pos[0] - 1 >= 0 and self.visited[pos[1]][pos[0] - 1] == 0:
            output.append(3)
        if pos[0] + 1 < self.width and self.visited[pos[1]][pos[0] + 1] == 0:
            output.append(1)
        if pos[1] - 1 >= 0 and self.visited[pos[1] - 1][pos[0]] == 0:
            output.append(0)
        if pos[1] + 1 < self.height and self.visited[pos[1] + 1][pos[0]] == 0:
            output.append(2)
        return output

    def scramble(self) -> None:
        """
        removes random walls in the maze before generation in case of unperfect
        maze
        """
        nb_remove: int = int(sqrt(random.randint(1, self.height * self.width)))
        i: int = 0
        current: tuple[int, int]
        while (i < nb_remove + 5):
            current = (random.randint(0, self.width - 1),
                       random.randint(0, self.height - 1))
            if not self.visited[current[1]][current[0]]:
                neighbors: list[int] = self.neighbors(current)
                random.shuffle(neighbors)
                self.dig_wall(current, neighbors[0])
            i += 1

    def remove_square_holes(self) -> None:
        """
        removes hole larger than 2*3 by filling the center with 3 walls
        """
        for line in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.lst_repr[line][col] == 0 and \
                    not (self.lst_repr[line - 1][col] & 8 or
                         self.lst_repr[line - 1][col] & 2) and \
                    not (self.lst_repr[line][col - 1] & 1 or
                         self.lst_repr[line][col - 1] & 4) and \
                    not (self.lst_repr[line + 1][col] & 8 or
                         self.lst_repr[line + 1][col] & 2) and \
                    not (self.lst_repr[line][col + 1] & 1 or
                         self.lst_repr[line][col + 1] & 4):
                    self.lst_repr[line][col] = random.choice([7, 11, 13, 15])

    def dfs(self) -> None:
        """
        uses randomized depth first search algorithm to genarate th maze
        """
        self.shape_stamp()
        self.ft_stamp(True)

        if not self.is_perfect:
            self.scramble()

        pos: list[tuple[int, int]] = [self.entry]
        while pos:
            self.visited[pos[-1][1]][pos[-1][0]] = 1
            if pos[-1] == self.exit:
                pos.pop()
                continue
            neighbors: list[int] = self.neighbors(pos[-1])
            if not neighbors:
                pos.pop()
                continue

            random.shuffle(neighbors)
            self.dig_wall(pos[-1], neighbors[0])
            if neighbors[0] == 0:
                pos.append((pos[-1][0], pos[-1][1] - 1))
            if neighbors[0] == 1:
                pos.append((pos[-1][0] + 1, pos[-1][1]))
            if neighbors[0] == 2:
                pos.append((pos[-1][0], pos[-1][1] + 1))
            if neighbors[0] == 3:
                pos.append((pos[-1][0] - 1, pos[-1][1]))
        self.remove_square_holes()


class AStar:
    """
    AStar is a class that aims to solve mazes generated with the MazeGen obj
    it must be instanciate before use
    init only takes a maze as a parameter
    """

    def __init__(self, maze: MazeGen):
        self.open = [maze.entry]
        self.closed: set[tuple[int, int]] = set()
        self.came_from: dict[tuple[int, int], tuple[int, int]] = dict()
        self.g = {maze.entry: 0}
        self.f = {maze.entry: self.dist(maze.entry, maze.exit)}

    @staticmethod
    def dist(src: tuple[int, int], dest: tuple[int, int]) -> int:
        """
        calculates the manathan distance between two nodes
        """
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

    @staticmethod
    def neighbors(maze: MazeGen, pos: tuple[int, int]) \
            -> list[tuple[int, int]]:
        """
        return the coordinate of the avaible neighbors from 'pos' cell
        """
        neighbors_coords: list[tuple[int, int]] = []
        walls: int = maze.lst_repr[pos[1]][pos[0]]

        if not walls & 1:
            neighbors_coords.append((pos[0], pos[1] - 1))
        if not walls & 2:
            neighbors_coords.append((pos[0] + 1, pos[1]))
        if not walls & 4:
            neighbors_coords.append((pos[0], pos[1] + 1))
        if not walls & 8:
            neighbors_coords.append((pos[0] - 1, pos[1]))
        return neighbors_coords

    def best_node(self) -> tuple[int, int]:
        """
        finds the node with the lowest f value
        """
        best_node = self.open[0]
        for node in self.open[1:]:
            if self.f[best_node] > self.f[node]:
                best_node = node
        return best_node

    def close_node(self, current: tuple[int, int]) -> None:
        """
        shift my current node from self.open to self.closed
        """
        self.open.remove(current)
        self.closed.add(current)

    def compare_paths(self, current: tuple[int, int], next: tuple[int, int]) \
            -> bool:
        """
        takes in a node and where we are trying to establish a path from
        and return true if the path should be established
        (true if no path to this cell exists or if it exists and is longer)
        """
        if next not in self.open and next not in self.g:
            return True
        if self.g[next] > self.g[current] + 1:
            return True
        return False

    def solve_paths(self, maze: MazeGen) -> bool:
        """
        finds a path from entry to exit
        puts every explored path in self.came_from
        """
        current: tuple[int, int]
        while self.open:
            current = self.best_node()
            self.close_node(current)
            if current == maze.exit:
                return True
            neighbors = self.neighbors(maze, current)
            for node in neighbors:
                if node in self.closed:
                    continue
                if self.compare_paths(current, node):
                    if node not in self.open:
                        self.open.append(node)
                    self.g[node] = self.g[current] + 1
                    self.f[node] = self.g[node] + \
                        self.dist(node, maze.exit)
                    self.came_from[node] = current
        return False

    def find_path(self, maze: MazeGen) -> str:
        """
        parse the came_from dict to find the best path from entry to exit
        """
        output: str = ""
        current: tuple[int, int] = maze.exit
        while current in self.came_from:
            if self.came_from[current][0] > current[0]:
                output += "W"
            elif self.came_from[current][0] < current[0]:
                output += "E"
            elif self.came_from[current][1] > current[1]:
                output += "N"
            elif self.came_from[current][1] < current[1]:
                output += "S"
            current = self.came_from[current]
        return output[::-1]

    def solve(self, maze: MazeGen) -> str | None:
        """
        solves a given maze using the A* algorithm
        output the solution from entry in a string formated with maze notation
        (N, S, E, W)
        """
        if self.solve_paths(maze):
            return self.find_path(maze)
        else:
            return None

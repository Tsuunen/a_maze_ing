import random
from math import sqrt
from ..config.parser import Config
from ..maze.parser import Maze


class MazeGen:
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
        self.shape = "ellipse"
        self.lst_repr = [[15 for i in range(self.width)]
                         for j in range(self.height)]

    def project_in(self) -> None:
        while self.lst_repr[self.entry[1]][self.entry[0]] == -1:
            if self.entry[0] < self.width // 2:
                self.entry = (self.entry[0] + 1, self.entry[1])
            else:
                self.entry = (self.entry[0] - 1, self.entry[1])
            if self.entry[1] < self.height // 2:
                self.entry = (self.entry[0], self.entry[1] + 1)
            else:
                self.entry = (self.entry[0], self.entry[1] - 1)

        while self.lst_repr[self.exit[1]][self.exit[0]] == -1:
            if self.exit[0] < self.width // 2:
                self.exit = (self.exit[0] + 1, self.exit[1])
            else:
                self.exit = (self.exit[0] - 1, self.exit[1])
            if self.exit[1] < self.height // 2:
                self.exit = (self.exit[0], self.exit[1] + 1)
            else:
                self.exit = (self.exit[0], self.exit[1] - 1)

    def shape_stamp(self) -> None:
        self.visited = [[0 for i in range(self.width)]
                        for j in range(self.height)]
        if self.shape == "rectangle":
            return

        if self.shape in ["square", "circle", "donut", "diamond"]:
            size: int = min(self.height, self.width)
            if self.entry[0] > size or self.entry[1] > size or \
               self.exit[0] > size or self.exit[1] > size:
                print("Error: cannot generate this maze shape(entry or \
exit outside the shape)")
                return
            self.width, self.height = size, size
            self.lst_repr = [[15 for i in range(self.width)]
                             for j in range(self.height)]
            self.visited = [[0 for i in range(self.width)]
                            for j in range(self.height)]

        if self.shape in ["circle", "donut"]:
            center: tuple[int, int] = (size // 2, size // 2)
            for line in range(size):
                for col in range(size):
                    if sqrt((center[0] - line)**2 + (center[1] - col)**2) \
                         > size // 2:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_in()

        if self.shape == "diamond":
            from .solver import AStar
            center: tuple[int, int] = (size // 2, size // 2)
            for line in range(size):
                for col in range(size):
                    if AStar.dist(center, (col, line)) > size // 2:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            self.project_in()

        if self.shape == "ellipse":
            center: tuple[int, int] = (self.width // 2, self.height // 2)
            for line in range(self.height):
                for col in range(self.width):
                    if (col - center[0]) ** 2 / center[0] ** 2 + \
                       (line - center[1]) ** 2 / center[1] ** 2 > 1:
                        self.lst_repr[line][col] = -1
                        self.visited[line][col] = -1
            for i in self.visited:
                for j in i:
                    print(j if j == 0 else 1, end="")
                print("\n")
            self.project_in()

    def ft_stamp(self, error: bool) -> None:
        """
        put the '42 stamp' on the maze if possible
        """
        if self.width < 9 or self.height < 7:
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

    @staticmethod
    def hexa(x: int) -> str | None:
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
            return None

    def __repr__(self, error: bool):
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

    def export_maze_file(self):
        """
        export the list representation of the maze in a .txt file
        """
        with open(self.output_file, "w") as f:
            f.write(self.__repr__(1))

    def export_maze_obj(self) -> None:
        repr = self.__repr__(0)
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
        from .solver import AStar
        solver: AStar = AStar(self)
        return solver.solve(self)

    def dig_wall(self, pos: list[int, int], direction: int) -> None:
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

    def neighbors(self, pos: list[int, int]) -> list[int]:
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
        self.visited[self.exit[1]][self.exit[0]] = 1
        self.ft_stamp(1)

        if not self.is_perfect:
            self.scramble()

        pos: list[tuple[int, int]] = [self.entry]
        while pos:
            self.visited[pos[-1][1]][pos[-1][0]] = 1
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

        for line in range(self.height):
            for col in range(self.width):
                if self.visited[line][col] == 1:
                    self.visited[line][col] = 0

        self.ft_stamp(0)
        self.dig_wall(self.exit, random.choice(self.neighbors(self.exit)))
        self.visited = None

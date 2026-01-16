import random
import sys
"""
0 north (up    / -y)(1)
1 east  (right / +x)(2)
2 south (down  / +y)(4)
3 west  (left  / -x)(8)
"""


class Maze:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.lst_repr = [[15 for i in range(width)] for j in range(height)]

    @staticmethod
    def hexa(x: int) -> str | None:
        """
        takes an integer and return it's hexadecimal representation
        """
        hexa = ["0", "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "A", "B", "C", "D", "E", "F"]
        try:
            return hexa[x]
        except Exception:
            return None

    def __repr__(self):
        repr = ""
        for i in self.lst_repr:
            for j in i:
                repr += self.hexa(j)
            repr += "\n"
        return repr

    def export_maze(self):
        """
        export the list representation of the maze in a .txt file
        """
        with open("output.txt", "w") as f:
            f.write(self.__repr__())

    def dig_wall(self, pos: list[int, int], direction: int) -> None:
        """
        given a pos and a dirrection,
        removes the wall between a position and the destination
        """
        if direction == 0:
            self.lst_repr[pos[1]][pos[0]] -= 1
            self.lst_repr[pos[1] - 1][pos[0]] -= 4
        elif direction == 1:
            self.lst_repr[pos[1]][pos[0]] -= 2
            self.lst_repr[pos[1]][pos[0] + 1] -= 8
        elif direction == 2:
            self.lst_repr[pos[1]][pos[0]] -= 4
            self.lst_repr[pos[1] + 1][pos[0]] -= 1
        elif direction == 3:
            self.lst_repr[pos[1]][pos[0]] -= 8
            self.lst_repr[pos[1]][pos[0] - 1] -= 2

    def neighbors(self, pos: list[int, int]) -> list[int]:
        """
        takes a pos in the currently generating maze (pos[x, y])
        return the list of unexplored neighbors
        """
        if pos[0] < 0 or pos[0] >= self.width or \
           pos[1] < 0 or pos[1] >= self.height:
            return []
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

    def dfs_core(self, pos: list[int, int]) -> None:
        """
        core of the backtracking function for the maze generation
        takes in a pos and creates random corridors
        should never be called alone
        """
        direction: int
        neighbors: list[int] = self.neighbors(pos)
        self.visited[pos[1]][pos[0]] = 1
        while len(neighbors) != 0:
            random.shuffle(neighbors)
            direction = neighbors.pop()
            self.dig_wall(pos, direction)
            if direction == 0:
                self.dfs_core([pos[0], pos[1] - 1])
            if direction == 1:
                self.dfs_core([pos[0] + 1, pos[1]])
            if direction == 2:
                self.dfs_core([pos[0], pos[1] + 1])
            if direction == 3:
                self.dfs_core([pos[0] - 1, pos[1]])
            neighbors = self.neighbors(pos)

    def dfs(self, seed: int = None) -> None:
        """
        Initialize depth first search genaration algorithm
        """
        random.seed(seed)
        self.visited = [[0 for i in range(self.width)]
                        for j in range(self.height)]
        self.dfs_core(self.entry)


if __name__ == "__main__":
    maze = Maze(50, 50, (0, 0), (50, 50))
    maze.dfs(26)
    sys.setrecursionlimit(100000000)
    maze.export_maze()

import random
import sys


class MazeGen:
    def __init__(self, width: int, height: int, entry: tuple[int:int],
                 exit: tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.lst_repr = [[15 for i in range(self.width)]
                         for j in range(self.height)]

    def ft_stamp_dfs(self) -> None:
        """
        put the '42 stamp' on the maze if possible
        """
        if self.width < 9 or self.height < 7:
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
            return hexa[x]
        except Exception:
            return None

    def __repr__(self):
        repr = ""
        for i in self.lst_repr:
            for j in i:
                repr += self.hexa(j)
            repr += "\n"
        repr += f"\n{self.entry[0]},{self.entry[1]}\n\
{self.exit[0]},{self.exit[1]}\n"
        print(self.solve())
        repr += self.solve()
        return repr

    def export_maze(self):
        """
        export the list representation of the maze in a .txt file
        """
        with open("output.txt", "w") as f:
            f.write(self.__repr__())

    def solve(self) -> str:
        """
        solve the maze
        return a string representing mooves necessary to solve it
        """
        from solver import AStar
        solver: AStar = AStar(self)
        return solver.solve(self)

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
        """
        if pos[0] < 0 or pos[0] >= self.width or \
           pos[1] < 0 or pos[1] >= self.height:
            return []
        #print(pos)
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
        self.ft_stamp_dfs()
        self.dfs_core(self.entry)


if __name__ == "__main__":
    maze = MazeGen(9, 7, (0, 0), (1, 1))
    maze.dfs()
    sys.setrecursionlimit(100000000)
    maze.export_maze()

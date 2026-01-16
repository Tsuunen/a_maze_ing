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
        try:
            repr += self.solve()
        except (TypeError):
            print("Maze with no solution cannot be represented")
            repr += ""
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

    def dfs(self, seed: int = None) -> None:
        """
        uses randomized depth first search algorithm to genarate th maze
        """
        random.seed(seed)
        self.visited = [[0 for i in range(self.width)]
                        for j in range(self.height)]
        self.ft_stamp_dfs()
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


if __name__ == "__main__":
    maze = MazeGen(69, 90, (0, 0), (50, 50))
    maze.dfs()
    sys.setrecursionlimit(100000000)
    maze.export_maze()

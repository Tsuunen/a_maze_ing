from maze_gen import Maze


class AStar:
    def __init__(self, maze: Maze):
        self.open = [maze.entry]
        self.closed = set()
        self.came_from = dict()
        self.g = {maze.entry: 0}
        self.f = {maze.entry: self.dist(maze.entry, maze.exit)}

    @staticmethod
    def dist(src: tuple[int, int], dest: tuple[int, int]) -> int:
        """
        calculates the manathan distance between two nodes
        """
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

    @staticmethod
    def unpack_neighbors(pos: tuple[int, int], neighbors: list[int]) \
            -> list[tuple[int, int]]:
        """
        converts neighbors from maze notation(direction)
        to solver notation(coordinates)
        """
        neighbors_coords = []
        for i in neighbors:
            if i == 0:
                neighbors_coords.append((pos[0], pos[1] - 1))
            elif i == 1:
                neighbors_coords.append((pos[0] + 1, pos[1]))
            elif i == 2:
                neighbors_coords.append((pos[0], pos[1] + 1))
            elif i == 3:
                neighbors_coords.append((pos[0] - 1, pos[1]))
        return neighbors_coords

    def best_node(self) -> tuple[int, int]:
        """
        finds the node with the lowest f value
        """
        if not self.open:
            return None
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

    def solve_paths(self, maze: Maze) -> bool:
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
            neighbors = self.unpack_neighbors(current, maze.neighbors(current))
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

    def find_path(self, maze: Maze) -> str:
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
                output += "S"
            elif self.came_from[current][1] < current[1]:
                output += "N"
            current = self.came_from[current]
        return output[::-1]

    def solve(self, maze: Maze) -> str | None:
        """
        solves a given maze using the A* algorithm
        output the solution from entry in a string formated with maze notation
        (N, S, E, W)
        """
        if self.solve_paths(maze):
            return self.find_path(maze)
        else:
            return None


if __name__ == "__main__":
    print(AStar.unpack_neighbors([5, 5], [0, 2]))

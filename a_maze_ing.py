from srcs.config.parser import ConfigParser
from srcs.maze.parser import MazeParser
from srcs.maze.maze import MazeDisplay
from srcs.generator.maze_gen import MazeGen


if (__name__ == "__main__"):
    try:
        parser = ConfigParser("config.txt")
    except Exception as e:
        print(e)
    config = parser.extract()
    print(config)
    maze = MazeGen(config)
    maze.dfs()
    maze.export_maze_file()
    print(maze.export_maze_obj())
    try:
        parser = MazeParser("maze.txt")
    except Exception as e:
        print(e)
    config = parser.extract()
    m = MazeDisplay(config)
    m.init()

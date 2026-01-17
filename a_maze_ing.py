from srcs.config.parser import ConfigParser
from srcs.maze.maze import MazeDisplay
from srcs.generator.maze_gen import MazeGen
from sys import argv


if (__name__ == "__main__"):
    if (len(argv) < 2):
        exit(1)
    try:
        parser = ConfigParser(argv[1])
        config = parser.extract()
        print(config)
        maze = MazeGen(config)
        maze.dfs()
        maze.export_maze_file()
        m = MazeDisplay(maze.export_maze_obj(), config)
        m.init()
    except Exception as e:
        print(e)

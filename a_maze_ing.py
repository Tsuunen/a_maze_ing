from srcs.config.parser import ConfigParser
from srcs.maze.maze import App
from srcs.generator.maze_gen import MazeGen
from sys import argv


if (__name__ == "__main__"):
    if (len(argv) < 2):
        exit(1)
    # try:
    parser = ConfigParser(argv[1])
    config = parser.extract()
    print(config)
    if (config is None):
        raise ValueError("The config is invalid")
    maze = MazeGen(config)
    maze.dfs()
    maze.export_maze_file()
    m = App(maze.export_maze_obj(), config)
    m.run()
    # except Exception as e:
    #     print(e)

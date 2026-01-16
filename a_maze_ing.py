from srcs.config.parser import ConfigParser
from srcs.maze.parser import MazeParser
from srcs.maze.maze import MazeDisplay
from srcs.generator.maze_gen import MazeGen


if (__name__ == "__main__"):
    # try:
    #     parser = ConfigParser("config.txt")
    # except Exception as e:
    #     print(e)
    # config = parser.extract()
    # print(config)
    try:
        parser = MazeParser("output.txt")
    except Exception as e:
        print(e)
    config = parser.extract()
    print(config)
    m = MazeDisplay(config)
    m.init()

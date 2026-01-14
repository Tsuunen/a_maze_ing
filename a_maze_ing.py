from srcs.config.parser import ConfigParser
from srcs.maze.parser import MazeParser
from srcs.maze.maze import MazeDisplay


if (__name__ == "__main__"):
    # try:
    #     parser = ConfigParser("config.txt")
    # except Exception as e:
    #     print(e)
    # config = parser.extract()
    # print(config)
    try:
        parser = MazeParser("maze2.txt")
    except Exception as e:
        print(e)
    config = parser.extract()
    print(config)
    # m = MazeDisplay("maze.txt")
    # m.init()

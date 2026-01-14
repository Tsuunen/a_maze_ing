# from srcs.config.parser import ConfigParser
from srcs.maze.maze import MazeDisplay


if (__name__ == "__main__"):
    # try:
    #     parser = ConfigParser("config.txt")
    # except Exception as e:
    #     print(e)
    # config = parser.extract()
    # print(config)
    m = MazeDisplay("nath.txt")
    m.init()
# m.draw()

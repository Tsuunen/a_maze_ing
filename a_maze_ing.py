# from srcs.config.parser import ConfigParser
from srcs.maze.maze import Maze


if (__name__ == "__main__"):
    # try:
    #     parser = ConfigParser("config.txt")
    # except Exception as e:
    #     print(e)
    # config = parser.extract()
    # print(config)
    m = Maze("maze.txt")
    m.init()
# m.draw()

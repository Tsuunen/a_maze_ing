from mlx import Mlx
from .parser import Maze
from ..config.parser import Config
from .help_display import HelpDisplay
from .maze_display import MazeDisplay

# zoom dans le maze avec scroll + grab


class App:
    def __init__(self, maze: Maze, config: Config):
        self.m = Mlx()
        self.mlx = self.m.mlx_init()

        self.maze_ui = MazeDisplay(self.m, self.mlx, maze, config)
        self.help_ui = HelpDisplay(self.m, self.mlx, self.maze_ui)

    def run(self):
        self.maze_ui.run()
        self.help_ui.run()
        self.m.mlx_loop(self.mlx)

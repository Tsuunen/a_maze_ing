from mlx import Mlx
from srcs.generator.maze_gen import Maze
from srcs.config.config_parser import Config
from .help_display import HelpDisplay
from .maze_display import MazeDisplay


class App:
    """Display orchestrator"""

    def __init__(self, maze: Maze, config: Config) -> None:
        self.m = Mlx()
        self.mlx = self.m.mlx_init()

        self.maze_ui = MazeDisplay(self.m, self.mlx, maze, config)
        self.help_ui = HelpDisplay(self.m, self.mlx, self.maze_ui)

    def run(self) -> None:
        """Run all the window
        """
        self.maze_ui.run()
        self.help_ui.run()
        self.m.mlx_loop(self.mlx)

    def destroy(self) -> None:
        """Clean and free all memory"""
        self.m.mlx_destroy_window(self.mlx, self.help_ui.win)
        self.m.mlx_destroy_window(self.mlx, self.maze_ui.win)
        self.m.mlx_destroy_image(self.mlx, self.maze_ui.img)

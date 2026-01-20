from random import randint, choice
from ..generator.maze_gen import MazeGen
from math import ceil
from .parser import Maze
from ..config.parser import Config
from mlx import Mlx
from typing import Any, Tuple


class MazeDisplay:
    def __init__(self, m: Mlx, mlx: Any, maze: Maze, config: Config) -> None:
        self.config = config
        # self.ratio = 8/10
        self.ratio = 3/10
        self.m = m
        self.mlx = mlx
        self.zoom = 1
        self._compute_geometry()
        self.win = self.m.mlx_new_window(self.mlx, self.width, self.win_height,
                                         "A Maze Ing - relaforg & nahecre")
        self._unpack_maze(maze)
        self._compute_img()
        self.show_path = True
        self.colors = [0x1ABC9CFF,
                       0x2ECC71FF,
                       0x3498DBFF,
                       0x9B59B6FF,
                       0x34495EFF,
                       0x16A085FF,
                       0x27AE60FF,
                       0x2980B9FF,
                       0x8E44ADFF,
                       0x2C3E50FF,
                       0xF1C40FFF,
                       0xE67E22FF,
                       0xE74C3CFF,
                       0xECF0F1FF,
                       0x95A5A6FF,
                       0x7F8C8DFF,
                       0xFFFFFFFF]
        self.wall_color = 0xFFFFFFFF
        self.logo_color = 0xFFFFFFFF
        self.tmp_config: Config | None = None
        self.drag_start: Tuple[int, int] | None = None
        self.offset: Tuple[int, int] = (0, 0)

    def _unpack_maze(self, maze: Maze) -> None:
        self.maze = maze.maze
        self.path = maze.path
        self.entry = maze.entry
        self.exit = maze.exit
        self.cols = maze.nbr_cols
        self.rows = maze.nbr_rows
        self.seed = maze.seed

    def _compute_geometry(self) -> None:
        (_, w, h) = self.m.mlx_get_screen_size(self.mlx)
        self.width = ceil(w * self.ratio)
        self.win_height = ceil(h * self.ratio)
        self.height = self.win_height - 50

    def _compute_img(self) -> None:
        self.cell_size = (min(self.width // self.cols,
                              self.height // self.rows) - 1) * self.zoom
        self.img_width = self.cols * self.cell_size + 1
        self.img_height = self.rows * self.cell_size + 1
        self.img = self.m.mlx_new_image(
            self.mlx, self.img_width, self.img_height)
        self.addr, bpp, self.line_len, _ = self.m.mlx_get_data_addr(self.img)
        self.bpp = bpp // 8

    def run(self) -> None:
        self.m.mlx_mouse_hook(self.win, self.on_mouse, None)
        self.m.mlx_key_hook(self.win, self.key_pressed, None)
        self.m.mlx_hook(self.win, 5, 1 << 3, self.on_mouse_release, None)
        self.m.mlx_hook(self.win, 33, 0,
                        lambda _: self.m.mlx_loop_exit(self.mlx), None)
        self.draw()
        self.refresh()

    def refresh(self) -> None:
        x: int = (self.width - self.cols *
                  self.cell_size) // 2 + self.offset[0]
        y: int = (self.height - self.rows *
                  self.cell_size) // 2 + self.offset[1]
        self.m.mlx_clear_window(self.mlx, self.win)
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img, x, y)
        self.m.mlx_string_put(self.mlx, self.win, 15, 10, 0xFFFFFFFF,
                              f"A Maze Ing - seed = {self.seed}")

    def on_mouse_release(self, button: int, x: int, y: int, _: Any) -> None:
        if (self.drag_start and button == 1):
            self.offset = (self.offset[0] + x - self.drag_start[0],
                           self.offset[1] + y - self.drag_start[1])
            self.refresh()
            self.drag_start = None

    def on_mouse(self, button: int, x: int, y: int, _: Any) -> None:
        change = False
        if (button == 1):
            self.drag_start = (x, y)
            self.is_draging = True
        if (button == 4):  # scroll up
            if (self.zoom < 5):
                self.zoom += 1
                change = True
        elif (button == 5):  # scroll down
            if (self.zoom > 1):
                self.zoom -= 1
                change = True
        if (change and button in [4, 5]):
            self._compute_img()
            self.draw()
            self.refresh()

    def key_pressed(self, keycode: int, _: Any) -> None:
        if (keycode == 113):  # 'q'
            self.m.mlx_loop_exit(self.mlx)
        elif (keycode == 112):  # 'p'
            self.toggle_path()
        elif (keycode == 114):  # 'r'
            self.regen_maze(self.config)
        elif (keycode == 119):  # 'w'
            self.change_wall_color()
        elif (keycode == 108):  # 'l'
            self.change_logo_color()
        elif (keycode == 116):  # 't'
            self.regen_maze(self.gen_random_config())
        elif (keycode == 120):  # 'x'
            self.export_config()
        elif (keycode == 61):  # '='
            self.ratio += 1/10
            self.recreate_win()
        elif (keycode == 45):  # '-'
            if (self.ratio > 0.4):
                self.ratio -= 1/10
                self.recreate_win()

    def recreate_win(self) -> None:
        self.m.mlx_destroy_window(self.mlx, self.win)
        self._compute_geometry()
        self.win = self.m.mlx_new_window(self.mlx, self.width, self.win_height,
                                         "A Maze Ing - relaforg & nahecre")
        self._compute_img()
        self.run()

    def change_wall_color(self) -> None:
        self.wall_color = choice(self.colors)
        self.draw()
        self.refresh()

    def change_logo_color(self) -> None:
        self.logo_color = choice(self.colors)
        self.draw()
        self.refresh()

    def regen_maze(self, config: Config) -> None:
        self.tmp_config = config
        gen = MazeGen(config)
        gen.dfs()
        maze = gen.export_maze_obj()
        self._unpack_maze(maze)
        self._compute_geometry()
        self._compute_img()
        self.m.mlx_clear_window(self.mlx, self.win)
        self.draw()
        self.refresh()

    def gen_random_config(self) -> Config:
        self.m.mlx_clear_window(self.mlx, self.win)
        width = randint(2, 250)
        height = randint(2, 250)
        entry = (randint(0, width - 1), randint(0, height - 1))
        exit = (randint(0, width - 1), randint(0, height - 1))
        return (Config(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            output_file="maze.txt",
            perfect=choice([True, False]),
            shape=choice(["rectangle", "square", "circle",
                         "donut", "diamond", "ellipse"])
        ))

    def export_config(self) -> None:
        if self.tmp_config is None:
            conf = self.config
        else:
            conf = self.tmp_config
        try:
            with open("config.txt", "w") as file:
                file.write(f"WIDTH={conf.width}\n")
                file.write(f"HEIGHT={conf.height}\n")
                file.write(f"ENTRY={conf.entry[0]}, {conf.entry[1]}\n")
                file.write(f"EXIT={conf.exit[0]}, {conf.exit[1]}\n")
                file.write(f"OUTPUT_FILE={conf.output_file}\n")
                file.write(f"PERFECT={conf.perfect}\n")
                if (conf.seed):
                    file.write(f"SEED={conf.seed}\n")
                else:
                    file.write(f"SEED={self.seed}\n")
                if (conf.shape):
                    file.write(f"SHAPE={conf.shape}\n")
            print("Success: Configuration file successfully exported")
        except Exception:
            print("Error: Configuration file failed to export")

    def fill_img(self, color: int = 0x000000FF) -> None:
        px = bytes((
            (color >> 8) & 0xFF,
            (color >> 16) & 0xFF,
            (color >> 24) & 0xFF,
            color & 0xFF,
        ))
        self.addr[:] = px * (self.img_width * self.img_height)

    def toggle_path(self) -> None:
        if (self.show_path):
            self.fill_path(0x000000FF)
        else:
            self.fill_path()
        self.show_path = not self.show_path
        self.refresh()

    def draw(self) -> None:
        self.fill_img()
        x, y = 0, 0
        for line in self.maze.split("\n"):
            for c in line:
                if (c != ' '):
                    self.put_cell(c, x * self.cell_size, y * self.cell_size)
                x += 1
            x = 0
            y += 1
            self.fill_cell(self.entry[0] * self.cell_size, self.entry[1]
                           * self.cell_size, 0x00FF00FF)
            self.fill_cell(self.exit[0] * self.cell_size, self.exit[1]
                           * self.cell_size, 0xFF0000FF)
        if (self.show_path):
            self.fill_path()

    def _connect_south(self, x: int, y: int, color: int) -> None:
        if (self.cell_size == 2):
            self.put_pixel(x * self.cell_size + 1,
                           y * self.cell_size + 2, color)
        elif (self.cell_size == 3):
            self.put_line(x * self.cell_size + 1, y *
                          self.cell_size + self.cell_size, 2, color)
        else:
            for i in range(3):
                self.put_line(x * self.cell_size + 2, y *
                              self.cell_size + self.cell_size - 1 + i,
                              self.cell_size - 3, color)

    def _connect_north(self, x: int, y: int, color: int) -> None:
        if (self.cell_size == 2):
            self.put_pixel(x * self.cell_size + 1,
                           y * self.cell_size, color)
        elif (self.cell_size == 3):
            self.put_line(x * self.cell_size + 1, y *
                          self.cell_size, 2, color)
        else:
            for i in range(3):
                self.put_line(x * self.cell_size + 2, y *
                              self.cell_size - 1 + i,
                              self.cell_size - 3, color)

    def _connect_west(self, x: int, y: int, color: int) -> None:
        if (self.cell_size == 2):
            self.put_pixel(x * self.cell_size,
                           y * self.cell_size + 1, color)
        elif (self.cell_size == 3):
            self.put_col(x * self.cell_size, y *
                         self.cell_size + 1, 2, color)
        else:
            for i in range(3):
                self.put_col(x * self.cell_size - 1 + i, y *
                             self.cell_size + 2, self.cell_size - 3,
                             color)

    def _connect_east(self, x: int, y: int, color: int) -> None:
        if (self.cell_size == 2):
            self.put_pixel(x * self.cell_size + 2,
                           y * self.cell_size + 1, color)
        elif (self.cell_size == 3):
            self.put_col(x * self.cell_size + self.cell_size, y *
                         self.cell_size + 1, 2, color)
        else:
            for i in range(3):
                self.put_col(x * self.cell_size + self.cell_size - 1
                             + i, y * self.cell_size + 2,
                             self.cell_size - 3, color)

    def fill_path(self, color: int = 0xC0C0C0FF) -> None:
        x, y = self.entry[0], self.entry[1]
        for j in range(len(self.path)):
            if (self.path[j] == "S"):
                self._connect_south(x, y, color)
                y += 1
            elif (self.path[j] == "N"):
                self._connect_north(x, y, color)
                y -= 1
            elif (self.path[j] == "W"):
                self._connect_west(x, y, color)
                x -= 1
            elif (self.path[j] == "E"):
                self._connect_east(x, y, color)
                x += 1
            if (j != len(self.path) - 1):
                self.fill_cell(x * self.cell_size, y * self.cell_size, color)

    def put_cell(self, s: str, cell_x: int, cell_y: int) -> None:
        c = int(s, 16)
        if (c & 1):
            self.put_line(cell_x, cell_y, self.cell_size, self.wall_color)
        if ((c >> 1) & 1):
            self.put_col(cell_x + self.cell_size, cell_y,
                         self.cell_size + 1, self.wall_color)
        if ((c >> 2) & 1):
            self.put_line(cell_x, cell_y + self.cell_size,
                          self.cell_size + 1, self.wall_color)
        if ((c >> 3) & 1):
            self.put_col(cell_x, cell_y, self.cell_size, self.wall_color)
        if (c == 0xF):
            self.fill_cell(cell_x, cell_y, self.logo_color)

    def put_line(self, x: int, y: int, size: int,
                 color: int = 0xFFFFFFFF) -> None:
        for i in range(size):
            self.put_pixel(x + i, y, color)

    def put_col(self, x: int, y: int, size: int,
                color: int = 0xFFFFFFFF) -> None:
        for i in range(size):
            self.put_pixel(x, y + i, color)

    def fill_cell(self, cell_x: int, cell_y: int,
                  color: int = 0xFFFFFFFF) -> None:
        if (self.cell_size == 2):
            self.put_pixel(cell_x + 1, cell_y + 1, color)
        elif (self.cell_size == 3):
            for i in range(2):
                self.put_line(cell_x + 1, cell_y + 1 + i, 2, color)
        else:
            for i in range(self.cell_size - 3):
                self.put_line(cell_x + 2, cell_y + i + 2,
                              self.cell_size - 3, color)

    def put_pixel(self, x: int, y: int, color: int = 0xFFFFFFFF) -> None:
        if x < 0 or y < 0 or x >= self.img_width or y >= self.img_height:
            return
        offset = y * self.line_len + x * self.bpp

        self.addr[offset] = (color >> 8) & 0xFF
        self.addr[offset + 1] = (color >> 16) & 0xFF
        self.addr[offset + 2] = (color >> 24) & 0xFF
        self.addr[offset + 3] = color & 0xFF

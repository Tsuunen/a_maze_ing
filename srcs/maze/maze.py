from mlx import Mlx
from pathlib import Path
import os


class Maze:
    def __init__(self, file_path: str):
        if Path(file_path).is_file() and os.access(file_path, os.R_OK):
            self.file_path = file_path
        else:
            raise FileNotFoundError(
                f"{file_path} does not exist or is not readable")
        self.width = 1080
        self.height = 720
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(self.mlx, self.width, self.height,
                                         "A Maze Ing - relaforg & nahecre")
        self.img = self.m.mlx_new_image(self.mlx, self.width, self.height)
        self.addr, bpp, self.line_len, _ = self.m.mlx_get_data_addr(self.img)
        self.bpp = bpp // 8
        self.wall_color = 0xFFFFFFFF

    def init(self):
        self.m.mlx_hook(self.win, 33, 0,
                        lambda d: self.m.mlx_loop_exit(self.mlx), None)
        self.draw()
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img, 0, 0)
        self.m.mlx_loop(self.mlx)

    def draw(self):
        with open(self.file_path, "r") as file:
            x, y = 0, 0
            cell_size = self.get_maze_info()
            for line in file:
                line = line.rstrip("\n")
                if (not line):
                    break
                for c in line:
                    # self.put_pixel(x * self.width // cols,
                    #                y * self.height // rows, 0xFFFFFFFF)
                    self.put_cell(c, x * cell_size,
                                  y * cell_size, cell_size)
                    x += 1
                x = 0
                y += 1

    def put_cell(self, c: str, cell_x: int, cell_y: int,
                 cell_size: int) -> None:
        c = int(c, 16)
        if (c & 1):
            self.put_line(cell_x, cell_y, cell_size)
        if ((c >> 1) & 1):
            self.put_col(cell_x + cell_size, cell_y, cell_size)
        if ((c >> 2) & 1):
            self.put_line(cell_x, cell_y + cell_size, cell_size)
        if ((c >> 3) & 1):
            self.put_col(cell_x, cell_y, cell_size)

    def put_line(self, x: int, y: int, size: int):
        for i in range(size):
            self.put_pixel(x + i, y, self.wall_color)

    def put_col(self, x: int, y: int, size: int):
        for i in range(size):
            self.put_pixel(x, y + i, self.wall_color)

    def get_maze_info(self) -> tuple[int, int]:
        with open(self.file_path, "r") as file:
            cols = 0
            rows = 0
            for line in file:
                line = line.rstrip("\n")
                if (not line):
                    break
                rows += 1
                if (cols == 0):
                    cols = len(line)
        return (min(self.width // cols, self.height // rows) - 1)

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.line_len + x * self.bpp

        self.addr[offset] = (color >> 8) & 0xFF
        self.addr[offset + 1] = (color >> 16) & 0xFF
        self.addr[offset + 2] = (color >> 24) & 0xFF
        self.addr[offset + 3] = color & 0xFF

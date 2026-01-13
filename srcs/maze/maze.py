from mlx import Mlx
from pathlib import Path
import os


class MazeDisplay:
    def __init__(self, file_path: str):
        if Path(file_path).is_file() and os.access(file_path, os.R_OK):
            self.file_path = file_path
        else:
            raise FileNotFoundError(
                f"{file_path} does not exist or is not readable")
        self.width = 1080
        self.height = 720
        self.win_height = 820
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(self.mlx, self.width, self.win_height,
                                         "A Maze Ing - relaforg & nahecre")
        self.img = self.m.mlx_new_image(self.mlx, self.width, self.height)
        self.addr, bpp, self.line_len, _ = self.m.mlx_get_data_addr(self.img)
        self.bpp = bpp // 8

    def init(self):
        self.m.mlx_key_hook(self.win, self.key_pressed, None)
        self.m.mlx_string_put(self.mlx, self.win, 15, 10,
                              0xFFFFFFFF, "A Maze Ing")
        self.m.mlx_string_put(self.mlx, self.win, 15, 790, 0xFFFFFFFF,
                              "r: Regenerate a new maze    p: Toggle path    "
                              + "q: quit")
        self.m.mlx_hook(self.win, 33, 0,
                        lambda d: self.m.mlx_loop_exit(self.mlx), None)
        self.draw()
        cell_size, cols, rows = self.get_maze_info()
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img,
                                       (self.width - cols * cell_size) // 2,
                                       50 +
                                       (self.height - rows * cell_size) // 2)
        self.m.mlx_loop(self.mlx)

    def key_pressed(self, keycode: int, _):
        if (keycode == 113):  # 'q'
            self.m.mlx_loop_exit(self.mlx)
        elif (keycode == 112):  # 'p'
            print("Toggle path")
        elif (keycode == 114):  # 'r'
            print("Regenerate maze")

    def draw(self):
        with open(self.file_path, "r") as file:
            x, y = 0, 0
            cell_size, _, _ = self.get_maze_info()
            for line in file:
                line = line.rstrip("\n")
                if (not line):
                    break
                for c in line:
                    self.put_cell(c, x * cell_size,
                                  y * cell_size, cell_size)
                    x += 1
                x = 0
                y += 1
            count = 0
            for line in file:
                line = line.rstrip("\n")
                if (count < 2):
                    coords = line.split(",")
                    if (len(coords) != 2):
                        continue
                    coords = [int(c) for c in coords]
                    if (count == 0):
                        x, y = coords[0], coords[1]
                        self.fill_cell(coords[0] * cell_size, coords[1]
                                       * cell_size, cell_size, 0x00FF00FF)
                    else:
                        self.fill_cell(coords[0] * cell_size, coords[1]
                                       * cell_size, cell_size, 0xFF0000FF)
                    count += 1
                    continue
                for j in range(len(line)):
                    if (line[j] == "S"):
                        y += 1
                    elif (line[j] == "N"):
                        y -= 1
                    elif (line[j] == "W"):
                        x -= 1
                    elif (line[j] == "E"):
                        x += 1
                    if (j != len(line) - 1):
                        self.fill_cell(x * cell_size, y * cell_size,
                                       cell_size, 0xFFFFFF80)

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
        if (c == 0xF):
            self.fill_cell(cell_x, cell_y, cell_size)

    def put_line(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
        for i in range(size):
            self.put_pixel(x + i, y, color)

    def put_col(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
        for i in range(size):
            self.put_pixel(x, y + i, color)

    def fill_cell(self, cell_x: int, cell_y: int, cell_size: int,
                  color: int = 0xFFFFFFFF) -> None:
        for i in range(cell_size - 3):
            self.put_line(cell_x + 2, cell_y + i + 2, cell_size - 3, color)

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
        return ((min(self.width // cols, self.height // rows) - 1, cols, rows))

    def put_pixel(self, x: int, y: int, color: int = 0xFFFFFFFF) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.line_len + x * self.bpp

        self.addr[offset] = (color >> 8) & 0xFF
        self.addr[offset + 1] = (color >> 16) & 0xFF
        self.addr[offset + 2] = (color >> 24) & 0xFF
        self.addr[offset + 3] = color & 0xFF

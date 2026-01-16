from mlx import Mlx
from .parser import Maze

# Afficher le path en animé


class Button:
    def __init__(self, x, y, action, label):
        self.x = x
        self.y = y
        self.w = 10 * len(label)
        self.h = 20
        self.action = action
        self.label = label

    def contains(self, mx, my):
        return (
            self.x <= mx < self.x + self.w and
            self.y <= my < self.y + self.h
        )


class MazeDisplay:
    def __init__(self, maze: Maze):
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
        self.maze = maze.maze
        self.path = maze.path
        self.entry = maze.entry
        self.exit = maze.exit
        self.cols = maze.nbr_cols
        self.rows = maze.nbr_rows
        self.cell_size = min(self.width // self.cols,
                             self.height // self.rows) - 1
        self.show_path = True
        self.buttons = []
        tmp = 0
        raw_buts = [
            {
                "label": "r: Regenerate a new maze",
                "action": lambda: print("Regenerate a new maze...")
            },
            {
                "label": "p: Toggle path on and off",
                "action": self.toggle_path
            },
            {
                "label": "q: quit",
                "action": lambda: self.m.mlx_loop_exit(self.mlx)
            }
        ]
        for button in raw_buts:
            but = Button(15 + tmp, 790, button["action"], button["label"])
            tmp += but.w + 40
            self.buttons.append(but)

    def init(self):
        self.m.mlx_key_hook(self.win, self.key_pressed, None)
        self.m.mlx_mouse_hook(self.win, self.on_mouse, None)
        self.m.mlx_string_put(self.mlx, self.win, 15, 10,
                              0xFFFFFFFF, "A Maze Ing")
        for i in self.buttons:
            self.m.mlx_string_put(self.mlx, self.win, i.x,
                                  i.y, 0xFFFFFFFF, i.label)
        self.m.mlx_hook(self.win, 33, 0,
                        lambda _: self.m.mlx_loop_exit(self.mlx), None)
        self.draw()
        self.refresh()
        self.m.mlx_loop(self.mlx)

    def refresh(self):
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img,
                                       (self.width - self.cols *
                                        self.cell_size) // 2,
                                       50 + (self.height - self.rows *
                                             self.cell_size) // 2)

    def on_mouse(self, button, x, y, _):
        for i in self.buttons:
            if (i.contains(x, y)):
                i.action()
                return

    def key_pressed(self, keycode: int, _):
        if (keycode == 113):  # 'q'
            self.m.mlx_loop_exit(self.mlx)
        elif (keycode == 112):  # 'p'
            self.toggle_path()
        elif (keycode == 114):  # 'r'
            print("Regenerate maze")

    def toggle_path(self):
        if (self.show_path):
            self.fill_path(0x000000FF)
        else:
            self.fill_path()
        self.show_path = not self.show_path
        self.refresh()

    def draw(self):
        self.fill_path()
        x, y = 0, 0
        for line in self.maze.split("\n"):
            for c in line:
                if (c != ' '):
                    self.put_cell(c, x * self.cell_size,
                                  y * self.cell_size)
                x += 1
            x = 0
            y += 1
            self.fill_cell(self.entry[0] * self.cell_size, self.entry[1]
                           * self.cell_size, 0x00FF00FF)
            self.fill_cell(self.exit[0] * self.cell_size, self.exit[1]
                           * self.cell_size, 0xFF0000FF)

    def fill_path(self, color: int = 0xFFFFFF80):
        x, y = self.entry[0], self.entry[1]
        for j in range(len(self.path)):
            if (self.path[j] == "S"):
                for i in range(3):
                    self.put_line(x * self.cell_size + 2, y *
                                  self.cell_size + self.cell_size - 1 + i,
                                  self.cell_size - 3, color)
                y += 1
            elif (self.path[j] == "N"):
                for i in range(3):
                    self.put_line(x * self.cell_size + 2, y *
                                  self.cell_size - 1 + i,
                                  self.cell_size - 3, color)
                y -= 1
            elif (self.path[j] == "W"):
                for i in range(3):
                    self.put_col(x * self.cell_size - 1 + i, y *
                                 self.cell_size + 2, self.cell_size - 3, color)
                x -= 1
            elif (self.path[j] == "E"):
                for i in range(3):
                    self.put_col(x * self.cell_size + self.cell_size - 1 + i,
                                 y * self.cell_size + 2, self.cell_size - 3,
                                 color)
                x += 1
            if (j != len(self.path) - 1):
                self.fill_cell(x * self.cell_size, y * self.cell_size, color)

    def put_cell(self, c: str, cell_x: int, cell_y: int) -> None:
        c = int(c, 16)
        if (c & 1):
            self.put_line(cell_x, cell_y, self.cell_size)
        if ((c >> 1) & 1):
            self.put_col(cell_x + self.cell_size, cell_y, self.cell_size + 1)
        if ((c >> 2) & 1):
            self.put_line(cell_x, cell_y + self.cell_size, self.cell_size + 1)
        if ((c >> 3) & 1):
            self.put_col(cell_x, cell_y, self.cell_size)
        if (c == 0xF):
            self.fill_cell(cell_x, cell_y)

    def put_line(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
        for i in range(size):
            self.put_pixel(x + i, y, color)

    def put_col(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
        for i in range(size):
            self.put_pixel(x, y + i, color)

    def fill_cell(self, cell_x: int, cell_y: int,
                  color: int = 0xFFFFFFFF) -> None:
        for i in range(self.cell_size - 3):
            self.put_line(cell_x + 2, cell_y + i + 2,
                          self.cell_size - 3, color)

    def put_pixel(self, x: int, y: int, color: int = 0xFFFFFFFF) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.line_len + x * self.bpp

        self.addr[offset] = (color >> 8) & 0xFF
        self.addr[offset + 1] = (color >> 16) & 0xFF
        self.addr[offset + 2] = (color >> 24) & 0xFF
        self.addr[offset + 3] = color & 0xFF

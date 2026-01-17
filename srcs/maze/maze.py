from mlx import Mlx
from .parser import Maze
from ..generator.maze_gen import MazeGen
from ..config.parser import Config
from random import randint, choice

# Afficher le path en animé
# generer des maze aleatoire et conserver un affichage responsive
# Essayer de faire une fenetre plus ou moins grande en fonction de la taille de l'ecran
# Afficher la seed en haut a droite de l'écran
# Si affichage relatif a la taille de la fenetre rajouter des raccourcis pour agrandir/rapetissir la fenetre


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
    def __init__(self, maze: Maze, config: Config):
        self.config = config
        self.width = 1080
        self.height = 720
        self.win_height = 820
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(self.mlx, self.width, self.win_height,
                                         "A Maze Ing - relaforg & nahecre")
        self.maze = maze.maze
        self.path = maze.path
        self.entry = maze.entry
        self.exit = maze.exit
        self.cols = maze.nbr_cols
        self.rows = maze.nbr_rows
        self.cell_size = min(self.width // self.cols,
                             self.height // self.rows) - 1
        self.img_width = self.cols * self.cell_size + 1
        self.img_height = self.rows * self.cell_size + 1
        self.img = self.m.mlx_new_image(
            self.mlx, self.img_width, self.img_height)
        self.addr, bpp, self.line_len, _ = self.m.mlx_get_data_addr(self.img)
        self.bpp = bpp // 8
        self.show_path = True
        self.buttons = []
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
                       0x7F8C8DFF,]
        self.wall_color = 0xFFFFFFFF
        self.logo_color = 0xFFFFFFFF
        tmp = 0
        raw_buts = [
            {
                "label": "r: New maze",
                "action": self.regen_maze
            },
            {
                "label": "p: Toggle path on and off",
                "action": self.toggle_path
            },
            {
                "label": "w: change wall color",
                "action": self.change_wall_color
            },
            {
                "label": "l: Change 42 color",
                "action": self.change_logo_color
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
        self.m.mlx_hook(self.win, 33, 0,
                        lambda _: self.m.mlx_loop_exit(self.mlx), None)
        self.m.mlx_string_put(self.mlx, self.win, 15, 10,
                              0xFFFFFFFF, "A Maze Ing")
        for i in self.buttons:
            self.m.mlx_string_put(self.mlx, self.win, i.x,
                                  i.y, 0xFFFFFFFF, i.label)
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
            self.regen_maze()
        elif (keycode == 119):
            self.change_wall_color()
        elif (keycode == 108):
            self.change_logo_color()

    def change_wall_color(self):
        self.wall_color = choice(self.colors)
        self.draw()
        self.refresh()

    def change_logo_color(self):
        self.logo_color = choice(self.colors)
        self.draw()
        self.refresh()

    def regen_maze(self):
        gen = MazeGen(self.config)
        gen.dfs()
        maze = gen.export_maze_obj()
        self.maze = maze.maze
        self.path = maze.path
        self.fill_img()
        self.draw()
        self.refresh()

    def fill_img(self, color: int = 0x000000FF):
        px = bytes((
            (color >> 8) & 0xFF,
            (color >> 16) & 0xFF,
            (color >> 24) & 0xFF,
            color & 0xFF,
        ))
        self.addr[:] = px * (self.img_width * self.img_height)

    def toggle_path(self):
        if (self.show_path):
            self.fill_path(0x000000FF)
        else:
            self.fill_path()
        self.show_path = not self.show_path
        self.refresh()

    def draw(self):
        if (self.show_path):
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

    def fill_path(self, color: int = 0xC0C0C0FF):
        x, y = self.entry[0], self.entry[1]
        for j in range(len(self.path)):
            if (self.path[j] == "S"):
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
                y += 1
            elif (self.path[j] == "N"):
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
                y -= 1
            elif (self.path[j] == "W"):
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
                x -= 1
            elif (self.path[j] == "E"):
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
                x += 1
            if (j != len(self.path) - 1):
                self.fill_cell(x * self.cell_size, y * self.cell_size, color)

    def put_cell(self, c: str, cell_x: int, cell_y: int) -> None:
        c = int(c, 16)
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

    def put_line(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
        for i in range(size):
            self.put_pixel(x + i, y, color)

    def put_col(self, x: int, y: int, size: int, color: int = 0xFFFFFFFF):
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
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.line_len + x * self.bpp

        self.addr[offset] = (color >> 8) & 0xFF
        self.addr[offset + 1] = (color >> 16) & 0xFF
        self.addr[offset + 2] = (color >> 24) & 0xFF
        self.addr[offset + 3] = color & 0xFF

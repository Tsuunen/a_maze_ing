from .button import Button
from time import sleep
from .maze_display import MazeDisplay
from mlx import Mlx
from typing import Any, TypedDict, Callable


class RawButton(TypedDict):
    label: str
    action: Callable[[], Any]


class HelpDisplay:
    def __init__(self, m: Mlx, mlx: Any, display: MazeDisplay) -> None:
        PAD_X = 30
        GAP_Y = 20
        self.display = display
        self.m = m
        self.mlx = mlx
        self.raw_buts: list[RawButton] = [
            {
                "label": "r: Generate a new maze",
                "action": lambda: display.regen_maze(display.config)
            },
            {
                "label": "t: Generate a new random maze",
                "action": lambda: display.regen_maze(
                    display.gen_random_config())
            },
            {
                "label": "x: export current maze config",
                "action": display.export_config
            },
            {
                "label": "p: Toggle path",
                "action": display.toggle_path
            },
            {
                "label": "w: Change wall color",
                "action": display.change_wall_color
            },
            {
                "label": "l: Change 42 color",
                "action": display.change_logo_color
            },
            {
                "label": "o: Reset maze",
                "action": display.reset_maze
            },
            {
                "label": "q: Quit",
                "action": lambda: display.m.mlx_loop_exit(self.mlx)
            }
        ]
        self.buttons = []
        tmp = GAP_Y
        for button in self.raw_buts:
            but = Button(PAD_X, tmp + GAP_Y,
                         button["action"], button["label"])
            tmp += but.h + GAP_Y
            self.buttons.append(but)
        self.win = self.m.mlx_new_window(self.mlx,
                                         max(b.w for b in self.buttons) +
                                         PAD_X * 2, GAP_Y + len(self.buttons) *
                                         20 + (len(self.buttons) - 1) *
                                         GAP_Y + GAP_Y * 2,
                                         "Help - relaforg & nahecre")

    def run(self) -> None:
        self.m.mlx_hook(self.win, 33, 0,
                        lambda _: self.m.mlx_loop_exit(self.mlx), None)
        self.m.mlx_mouse_hook(self.win, self.on_mouse, None)
        self.m.mlx_key_hook(self.win, self.key_pressed, None)
        self.m.mlx_string_put(self.mlx, self.win, 10, 10,
                              0xFFFFFFFF, "Help window")
        for i in self.buttons:
            sleep(0.001)
            self.m.mlx_string_put(self.mlx, self.win, i.x,
                                  i.y, 0xFFFFFFFF, i.label)

    def on_mouse(self, button: int, x: int, y: int, _: Any) -> None:
        if (button == 1):
            for i in self.buttons:
                if (i.contains(x, y)):
                    i.action()
                    return

    def key_pressed(self, keycode: int, _: Any) -> None:
        if (keycode == 113):  # 'q'
            self.m.mlx_loop_exit(self.mlx)
        elif (keycode == 112):  # 'p'
            self.display.toggle_path()
        elif (keycode == 114):  # 'r'
            self.display.regen_maze(self.display.config)
        elif (keycode == 119):  # 'w'
            self.display.change_wall_color()
        elif (keycode == 108):  # 'l'
            self.display.change_logo_color()
        elif (keycode == 116):  # 't'
            self.display.regen_maze(self.display.gen_random_config())
        elif (keycode == 120):  # 'x'
            self.display.export_config()
        elif (keycode == 111):  # 'o'
            self.display.reset_maze()
        elif (keycode == 61):  # '='
            self.display.ratio += 1/10
            self.display.recreate_win()
        elif (keycode == 45):  # '-'
            if (self.display.ratio > 0.4):
                self.display.ratio -= 1/10
                self.display.recreate_win()

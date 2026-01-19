from typing import Callable, Any


class Button:
    def __init__(self, x: int, y: int, action: Callable[[Any], Any],
                 label: str) -> None:
        self.x = x
        self.y = y
        self.w = 10 * len(label)
        self.h = 20
        self.action = action
        self.label = label

    def contains(self, mx: int, my: int) -> bool:
        """Check if the coords (mx, my) are in the button

        Keyword arguments:
        mx -- x coordinate
        my -- y coordinate
        """
        return (
            self.x <= mx < self.x + self.w and
            self.y <= my < self.y + self.h
        )

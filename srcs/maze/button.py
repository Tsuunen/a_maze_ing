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

from pynput import mouse

class MouseListener:
    def __init__(self, main):
        self.main = main

    def start_mouse_listener(self):
        return mouse.Listener(
                on_click=self.on_click,
                on_move=self.on_move,
                on_scroll=self.on_scroll
            )

    # Fonction pour capturer les événements de la souris
    def on_click(self, x, y, button, pressed):
        if pressed:
            left_or_right = "left"

            if str(button) == "Button.right":
                left_or_right = "right"

            self.main.send_data("click", x, y, 1, 0.0, left_or_right)

    def on_move(self, x, y):
        self.main.send_data("moveTo", x, y)

    def on_scroll(self, x, y, dx, dy):
        self.main.send_data("scroll", dy, x, y)



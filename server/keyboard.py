
from pynput import keyboard

class KeyboardListener:
    def __init__(self, main):
        self.main = main

    def start_keyboard_listener(self):
        return keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )

    # Fonction pour capturer les événements du clavier
    def on_press(self, key):
        try:
            data = key.char
        except AttributeError:
            data = key

        self.main.send_data("keyDown", data)

    def on_release(self, key):
        try:
            data = key.char
        except AttributeError:
            data = key

        self.main.send_data("keyUp", data)
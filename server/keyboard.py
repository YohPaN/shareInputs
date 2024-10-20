
from pynput import keyboard

class KeyboardListener:
    main = None

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

        self.main.buffer_event("keyDown", data)

    def on_release(self, key):
        try:
            data = key.char
        except AttributeError:
            data = key

        self.main.buffer_event("keyUp", data)
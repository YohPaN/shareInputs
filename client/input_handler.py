from pynput.keyboard import Controller as KeyboardController, Key
import json
import pyautogui
import logging

class InputHandler:
    # Configurer les contrôleurs pour simuler les actions
    keyboard = KeyboardController()

    def __init__(self):
        pass
    # Fonction pour interpréter les événements reçus et simuler les actions
    def process_event(self, data):
        if data:
            event_type = data['type']
            args = data['args']

            getattr(pyautogui, event_type)(*args)

        else:
            logging.warning("Empty or invalid data received, ignoring...")


   

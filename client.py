import socket
import pyautogui
from pynput.mouse import Button
from pynput.keyboard import Controller as KeyboardController, Key
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to INFO or WARNING for less verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format with time, level, and message
)

# Adresse IP et port du serveur Windows
SERVER_IP = '192.168.1.20'  # L'IP du PC Windows sur le réseau local
SERVER_PORT = 12345

# Créer un socket pour envoyer des données
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Configurer les contrôleurs pour simuler les actions
keyboard = KeyboardController()

# Fonction pour interpréter les événements reçus et simuler les actions
def process_event(data):
    if data.strip():
        try:
            event = json.loads(data)
            event_type = event['type']
            args = event['args']

            getattr(pyautogui, event_type)(*args)

        except json.JSONDecodeError as e:
            logging.error(f"JSONDecodeError: {e} - Data received: {data}")  # Log errors
    else:
        logging.warning("Empty or invalid data received, ignoring...")


# Boucle pour recevoir et traiter les événements
buffer = ""
while True:
    data = client_socket.recv(1024).decode()
    if not data:
        print("No data received, closing connection.", flush=True)
        break

    buffer += data  # Append data to the buffer
    while '\n' in buffer:  # Process complete lines (events)
        line, buffer = buffer.split('\n', 1)
        process_event(line)

client_socket.close()

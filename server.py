import socket
import time
import threading
from pynput import mouse, keyboard
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to INFO or WARNING for less verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format with time, level, and message
)

# Adresse IP et port du serveur Windows (pour recevoir les données)
HOST = '0.0.0.0'
PORT = 12345

# Créer un socket pour écouter les connexions
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print(f"Serveur en attente de connexion sur le port {PORT}...")

# Accepter une connexion
client_socket, client_address = sock.accept()
print(f"Connexion établie avec {client_address}")

# Buffer to hold events before sending
event_buffer = []

# Mutex to synchronize access to the event buffer
buffer_lock = threading.Lock()

# Function to send buffered events periodically
def send_buffered_events():
    while True:
        time.sleep(0.05)  # Send every 50 milliseconds
        with buffer_lock:
            if event_buffer:
                logging.info(event_buffer)
                data_to_send = ''.join(event_buffer)  # Combine all events into one string
                client_socket.sendall(data_to_send.encode())  # Send the batch
                event_buffer.clear()  # Clear the buffer after sending

# Start the thread that sends events in batches
threading.Thread(target=send_buffered_events, daemon=True).start()

# Function to add events to the buffer
def buffer_event(event_type, *args):
    event = {'type': event_type, 'args': args}

    with buffer_lock:
        event_buffer.append(json.dumps(event) + '\n')  # Add the event to the buffer

# Fonction pour capturer les événements de la souris
def on_click(x, y, button, pressed):
    if pressed:
        left_or_right = "left"

        if str(button) == "Button.right":
            left_or_right = "right"

        buffer_event("click", x, y, 1, 0.0, left_or_right)

def on_move(x, y):
    buffer_event("moveTo", x, y)

def on_scroll(x, y, dx, dy):
    buffer_event("scroll", dy, x, y)

# Fonction pour capturer les événements du clavier
def on_press(key):
    try:
        data = key.char
    except AttributeError:
        data = key

    buffer_event("keyDown", data)

def on_release(key):
    try:
        data = key.char
    except AttributeError:
        data = key

    buffer_event("keyUp", data)

# Lancement des listeners pour le clavier et la souris
with mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as mouse_listener, keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()

client_socket.close()
sock.close()

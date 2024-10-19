import socket
from config.config import Config
from client.main import MainClient
from client.input_handler import InputHandler


class Client:
    client_socket = None
    config = None

    def __init__(self, config: Config):
        # Créer un socket pour envoyer des données
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config

    def start(self):
        self.client_socket.connect((self.config.SERVER_IP, self.config.PORT))
        MainClient(self, InputHandler)

    def shutdown(self):
        self.client_socket.close()


    # # Configurer les contrôleurs pour simuler les actions
    # keyboard = KeyboardController()

    # # Fonction pour interpréter les événements reçus et simuler les actions
    # def process_event(data):
    #     if data.strip():
    #         try:
    #             event = json.loads(data)
    #             event_type = event['type']
    #             args = event['args']

    #             getattr(pyautogui, event_type)(*args)

    #         except json.JSONDecodeError as e:
    #             logging.error(f"JSONDecodeError: {e} - Data received: {data}")  # Log errors
    #     else:
    #         logging.warning("Empty or invalid data received, ignoring...")


    # # Boucle pour recevoir et traiter les événements
    # buffer = ""
    # while True:
    #     data = client_socket.recv(1024).decode()
    #     if not data:
    #         print("No data received, closing connection.", flush=True)
    #         break

    #     buffer += data  # Append data to the buffer
    #     while '\n' in buffer:  # Process complete lines (events)
    #         line, buffer = buffer.split('\n', 1)
    #         process_event(line)


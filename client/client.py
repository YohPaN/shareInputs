import socket
from config.config import Config
from client.main import MainClient
from client.input_handler import InputHandler


class Client:
    client_socket = None
    config = None

    def __init__(self, config: Config, logger):
        # Créer un socket pour envoyer des données
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config

    def start(self):
        self.client_socket.connect((self.config.SERVER_IP, self.config.PORT))
        print("Connected")
        inputHandler = InputHandler()
        MainClient(self, inputHandler)

    def shutdown(self):
        self.client_socket.close()

import socket
from config.config import Config
from server.main import MainServer

class Server:
    client_socket = None
    client_address = None
    sock = None
    max_connection = 1
    config = None

    def __init__(self, config: Config, logger):
        # Créer un socket pour écouter les connexions
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config

    def start(self):
        self.sock.bind((self.config.HOST, self.config.PORT))
        self.sock.listen(self.max_connection)
        print(f"Serveur en attente de connexion sur le port {self.sock.getsockname()}...")

        # Accepter une connexion
        self.client_socket, self.client_address = self.sock.accept()
        print(f"Connexion établie avec {self.client_address}")
        
        main = MainServer(self)
        main.start_main()

    def shutdown(self):
        self.client_socket.close()
        self.sock.close()




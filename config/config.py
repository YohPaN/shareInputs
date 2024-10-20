import logging

# Adresse IP et port du serveur Windows (pour recevoir les données)
HOST = '0.0.0.0'
SERVER_IP = '192.168.1.20'  # L'IP du PC Windows sur le réseau local
PORT = 12345

def create_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # Set to INFO or WARNING for less verbose logging
        format='%(asctime)s - %(levelname)s - %(message)s'  # Format with time, level, and message
    )

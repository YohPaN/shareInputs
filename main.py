from config.config import create_logger
import logging
from server.server import Server
from client.client import Client
import sys

create_logger()
logger = logging.getLogger(__name__)

try:
    serverOrClient = sys.argv[1]
except IndexError:
    raise IndexError('Add an argument ("server" or "client")')

app = None

if serverOrClient == "server":
    app = Server(logger)
elif serverOrClient == "client":
    app = Client(logger)
else:
    exit()

app.start()
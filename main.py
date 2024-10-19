from config.config import Config
import logging
from server.server import Server
from client.client import Client

config = Config()
config.create_logger()
logger = logging.getLogger(__name__)

serverOrClient = "client"
app = None

if serverOrClient == "server":
    app = Server(config)
    print(app)
else:
    app = Client(config)
print("ready to start app")
app.start()
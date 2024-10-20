import asyncio
from client.input_handler import read_data
from config.config import PORT, SERVER_IP

class Client:
    def __init__(self, logger):
        self.logger = logger

    # Connect to the server
    def start(self):
        self.logger.debug("Starting the client...")
        asyncio.run(self.tcp_client())

    # main loop for waiting data from server
    async def tcp_client(self):
        try:
            reader, writer = await asyncio.open_connection(SERVER_IP, PORT)

            while True:
                data = await reader.read(10000)
                await read_data(data.decode(), self.logger)
                
        except ConnectionError:
            self.logger.warning('Impossible to connect to the server')
            raise ConnectionError('Impossible to connect to the server')
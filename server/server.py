import asyncio
from config.config import HOST, PORT
import threading
from server.mouse import MouseListener
from server.keyboard import KeyboardListener

class Server:
    writer = None
    
    def __init__(self, logger):
        self.logger = logger
        self.mouse_listener = MouseListener(self)
        self.keyboard_listener = KeyboardListener(self)

    def start(self):
        self.logger.debug("starting the server")

        asyncio.run(self.main())

    async def main(self):
        asyncio.create_task(self.start_mouse_and_keyboard_listener())

        server = await asyncio.start_server(self.handler, HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        self.logger.debug(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handler(self, reader, writer):
        self.writer = writer

        while True:
            await asyncio.sleep(1)
        
    def send_data(self, event_type, *args):
        event = {'type': event_type, 'args': args}
        self.writer.write(f"{event}/".encode('utf-8'))

    async def start_mouse_and_keyboard_listener(self):
        keyboard_listener = self.keyboard_listener.start_keyboard_listener()
        mouse_listener = self.mouse_listener.start_mouse_listener()

        await asyncio.to_thread(self.run_listener, 
                keyboard_listener,
                mouse_listener
            )


    def run_listener(self, keyboard_listener, mouse_listener):
        with keyboard_listener, mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

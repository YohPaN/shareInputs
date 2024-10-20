import asyncio
from config.config import HOST, PORT
import threading
from server.mouse import MouseListener
from server.keyboard import KeyboardListener

class Server:
    event_buffer = []
    
    def __init__(self, logger):
        self.logger = logger
        self.mouse_listener = MouseListener(self)
        self.keyboard_listener = KeyboardListener(self)

    def start(self):
        self.logger.debug("starting the server")

        # TODO: mettre le thread dans un asyncio.to_thread()
        threading.Thread(target=self.start_mouse_and_keyboard_listener, daemon=True).start()

        asyncio.run(self.main())

    async def main(self):
        server = await asyncio.start_server(self.handler, HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        self.logger.debug(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    # TODO: streamer directement les data au lieu de passer par un buffer
    async def handler(self, reader, writer):
        while True:
            if self.event_buffer:
                data_to_send = b''.join(self.event_buffer)
                writer.write(data_to_send)
                self.event_buffer.clear()

    # Function to add events to the buffer
    def buffer_event(self, event_type, *args):
        event = {'type': event_type, 'args': args}
        self.event_buffer.append(f"{event}/".encode('utf-8'))


    async def start_mouse_and_keyboard_listener(self):
        keyboard_listener = self.keyboard_listener.start_keyboard_listener()
        mouse_listener = self.mouse_listener.start_mouse_listener()

        with keyboard_listener, mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

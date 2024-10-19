
from config.config import Config
from server.keyboard import KeyboardListener
import threading
import time
import json
from server.mouse import MouseListener

class MainServer:
   
    # Buffer to hold events before sending
    event_buffer = []
    server = None
    mouse_listener = None
    keyboard_listener = None
    
    # Mutex to synchronize access to the event buffer
    buffer_lock = threading.Lock()

    def __init__(self, server):
        # voir si besoin de join les listener ici
        self.server = server
        self.mouse_listener = MouseListener(self)
        self.keyboard_listener = KeyboardListener(self)
        self.mouse_listener.start_mouse_listener()
        self.keyboard_listener.start_keyboard_listener()

        # Start the thread that sends events in batches
        threading.Thread(target=self.send_buffered_events, daemon=True).start()

    # Function to send buffered events periodically
    def send_buffered_events(self):
        while True:
            print('test')
            time.sleep(0.05)  # Send every 50 milliseconds
            with self.buffer_lock:
                if self.event_buffer:
                    data_to_send = ''.join(self.event_buffer)  # Combine all events into one string
                    self.server.client_socket.sendall(data_to_send.encode())  # Send the batch
                    self.event_buffer.clear()  # Clear the buffer after sending


    # Function to add events to the buffer
    def buffer_event(self, event_type, *args):
        event = {'type': event_type, 'args': args}

        with self.buffer_lock:
            self.event_buffer.append(json.dumps(event) + '\n')  # Add the event to the buffer


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

    def start_main(self):
        # Start the thread that sends events in batches
        threading.Thread(target=self.send_buffered_events, daemon=True).start()

        keyboard_listener = self.keyboard_listener.start_keyboard_listener()
        mouse_listener = self.mouse_listener.start_mouse_listener()

        with keyboard_listener, mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()
        
    # Function to send buffered events periodically
    def send_buffered_events(self):
        while True:
            time.sleep(0.05)  # Send every 50 milliseconds
            with self.buffer_lock:
                if self.event_buffer:
                    data_to_send = b''.join(self.event_buffer)  # Combine all events into one string
                    self.server.client_socket.sendall(data_to_send)  # Send the batch
                    self.event_buffer.clear()  # Clear the buffer after sending


    # Function to add events to the buffer
    def buffer_event(self, event_type, *args):
        event = {'type': event_type, 'args': args}

        with self.buffer_lock:
            self.event_buffer.append(f"{event}/".encode('utf-8'))  # Add the event to the buffer

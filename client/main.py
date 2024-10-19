class MainClient:
    client = None
    inputHandler = None
    buffer = ""

    def __init__(self, client, inputHandler):
        self.client = client
        self.inputHandler = inputHandler
        self.start_main()

    def start_main(self):
        while True:
            print('test')
            data = self.client.client_socket.recv(1024).decode()
            if not data:
                print("No data received, closing connection.", flush=True)
                break

            buffer += data  # Append data to the buffer
            while '\n' in buffer:  # Process complete lines (events)
                line, buffer = buffer.split('\n', 1)
                self.inputHandler.process_event(line)
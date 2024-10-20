import ast
class MainClient:
    client = None
    inputHandler = None

    def __init__(self, client, inputHandler):
        self.client = client
        self.inputHandler = inputHandler
        self.start_main()

    def start_main(self):
        buffer = ""

        while True:
            data = self.client.client_socket.recv(1024).decode()
            if not data:
                print("No data received, closing connection.", flush=True)
                break

            buffer += data  # Append data to the buffer
           
            while '/' in buffer:  # Process complete lines (events)
                line, buffer = buffer.split('/', 1)
                line = ast.literal_eval(line.strip())
                self.inputHandler.process_event(data=line)

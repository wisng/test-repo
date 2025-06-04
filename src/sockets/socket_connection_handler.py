from src.sockets.socket_base_handler import BaseSocketHandler


class ConnectionSocketHandler(BaseSocketHandler):
    """Handler for connection-related socket events."""

    def __init__(self, socketio, handlers=None):
        super().__init__(socketio)
        # Store references to other handlers that need client info
        self.handlers = handlers or []

    def add_handler(self, handler):
        """Add a handler that needs client registration."""
        self.handlers.append(handler)

    def register_events(self):
        """Register all connection-related socket events."""

        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected')

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected')
            # You may want to handle cleanup for specific clients here

        @self.socketio.on('identify')
        def identify_client(data):
            client_id = data.get('id')
            if client_id:
                print(f"Client identified: {client_id}")
                # Register client in this handler
                self.register_client(client_id, self.socketio)

                # Propagate client registration to other handlers
                for handler in self.handlers:
                    handler.register_client(client_id, self.socketio)

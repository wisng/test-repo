from flask_socketio import SocketIO


class SocketManager:
    def __init__(self):
        self.socketio = None
        self.handlers = []

    def create_socketio(self):
        """Create and return a SocketIO instance."""
        self.socketio = SocketIO(async_mode="eventlet")
        return self.socketio

    def init_app(self, app):
        """Initialize SocketIO with Flask application."""
        if self.socketio is None:
            self.socketio = self.create_socketio()

        self.socketio.init_app(app, cors_allowed_origins="*")
        print("SocketIO initialized")
        return self.socketio

    def get_socketio(self):
        """Get the SocketIO instance or create it if it doesn't exist."""
        if self.socketio is None:
            self.socketio = self.create_socketio()
        return self.socketio

    def register_handler(self, handler):
        """Register a socket handler."""
        self.handlers.append(handler)

    def initialize_handlers(self):
        """Initialize all registered handlers."""
        for handler in self.handlers:
            handler.register_events()
        print(f"Initialized {len(self.handlers)} socket handlers")

    def run(self, app, host="0.0.0.0", port=5100):
        """Run the SocketIO server."""
        if self.socketio is None:
            raise ValueError("SocketIO must be initialized before running")

        self.socketio.run(app, host=host, port=port)

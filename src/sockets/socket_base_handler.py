from typing import Dict
import socketio as client_socketio


class BaseSocketHandler:
    """Base class for all socket handlers."""

    def __init__(self, socketio):
        self.socketio = socketio
        self.clients: Dict[str, client_socketio.Client] = {}

    def register_client(self, client_id, client):
        """Register a client connection."""
        self.clients[client_id] = client

    def get_client(self, client_id):
        """Get a client by ID."""
        return self.clients.get(client_id)

    def register_events(self):
        """
        Abstract method to register events.
        This should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement register_events()")

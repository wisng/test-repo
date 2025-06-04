from flask import Flask
from flask_cors import CORS
from sockets.socket_connection_handler import ConnectionSocketHandler
from sockets.socket_voice_handler import VoiceSocketHandler
from src.routes.rest_routes import api
from src.config.settings import settings
from src.sockets.socket_manager import SocketManager


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    CORS(app, origins=["*"], supports_credentials=True)

    socket_manager = SocketManager()
    socketio = socket_manager.init_app(app)

    voice_handler = VoiceSocketHandler(socketio)

    connection_handler = ConnectionSocketHandler(socketio, handlers=[voice_handler])
    socket_manager.register_handler(connection_handler)

    socket_manager.register_handler(connection_handler)
    socket_manager.register_handler(voice_handler)
    socket_manager.initialize_handlers()

    print("Starting server...")
    return app, socketio


app, socketio = create_app()
if __name__ == '__main__':
    app.run(
        host=settings.flask.host,
        port=settings.flask.port
    )

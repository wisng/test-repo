from flask import Flask
from flask_socketio import SocketIO
from src.sockets.socket_relay_handler import SocketRelayHandler
from src.routes.rest_routes import api
from src.config.settings import settings


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    socketio = SocketIO()

    socketio.init_app(app, cors_allowed_origins="*")

    relay_handler = SocketRelayHandler(socketio)
    relay_handler.initialize_handlers()

    print("SocketIO initialized")
    return app, socketio


app, socketio = create_app()
if __name__ == '__main__':
    socketio.run(
        app,
        host=settings.flask.host,
        port=settings.flask.port
    )

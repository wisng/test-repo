from flask import Flask
from src.routes.rest_routes import api
from src.config.settings import settings


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    print("Starting server...")
    return app


app = create_app()
if __name__ == '__main__':
    app.run(
        host=settings.flask.host,
        port=settings.flask.port
    )

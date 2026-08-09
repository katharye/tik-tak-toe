from flask import Flask

from datasource.db import Base, engine
from di import Container, configure_container
from domain import GameServiceABC, IAuthService
from web import create_game_blueprint, create_auth_blueprint, UserAuthenticator

def create_app():
    Base.metadata.create_all(bind=engine)

    cn = Container()
    configure_container(cn)

    app = Flask(__name__)

    game_service = cn.resolve(GameServiceABC)
    game_bp = create_game_blueprint(game_service)
    app.register_blueprint(game_bp)

    auth_service = cn.resolve(IAuthService)
    auth_bp = create_auth_blueprint(auth_service)
    app.register_blueprint(auth_bp)

    authenticator = UserAuthenticator(auth_service)
    authenticator.register(app, exempt_blueprints=["auth"])
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
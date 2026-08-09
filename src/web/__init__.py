# web/__init__.py
from .route import GameRoute
from .route import create_game_blueprint, create_auth_blueprint, create_user_blueprint
from .authenticator import UserAuthenticator
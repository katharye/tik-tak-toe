# web/route/__init__.py
from .game_route import GameRoute, create_game_blueprint
from .auth_route import AuthRoute, create_auth_blueprint
from .user_route import UserRoute, create_user_blueprint
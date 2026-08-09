from flask import Blueprint, jsonify, g
from flask.views import MethodView

from typing import Optional

from domain import IPlayerRepository
from web.mapper import WebPlayerMapper

class UserRoute(MethodView):
    def __init__(self, player_repository: IPlayerRepository):
        self.player_repository = player_repository

    def get(self, user_id: Optional[str] = None):

        # GET /user/<user_id> — получить данные пользователя

        if user_id is None:
            player_id = g.current_user
            player = self.player_repository.get(player_id)
            if player is not None:
                dto =  WebPlayerMapper.to_web(player)
                return jsonify({
                    "id": str(dto.id),
                    "login": dto.login,
                }), 200

        player = self.player_repository.get(user_id)
        if player is not None:
            dto =  WebPlayerMapper.to_web(player)
            return jsonify({
                "id": str(dto.id),
                "login": dto.login,
            }), 200

        return jsonify({"error": "Not found"}), 404


def create_user_blueprint(player_repository: IPlayerRepository):
    bp = Blueprint('user', __name__, url_prefix='/user')
    view = UserRoute.as_view('user_route', player_repository=player_repository)
    bp.add_url_rule('/<user_id>', view_func=view, methods=['GET'])
    bp.add_url_rule('', view_func=view, methods=['GET'])
    return bp
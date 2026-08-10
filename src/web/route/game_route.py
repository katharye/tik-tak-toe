# web/route/game_route.py
from flask import g, Blueprint, jsonify, request
from flask.views import MethodView

from typing import Optional
from uuid import UUID

from domain import IGameService, GameType
from web.mapper import WebGameMapper, WebLiderBoardProfileMapper
from web.model import CreateGameRequestDTO, MoveRequestDTO

class GameRoute(MethodView):
    def __init__(self, game_service: IGameService):
        self.game_service = game_service

    def post(self, game_id: Optional[str] = None, action: Optional[str] = None):

        # POST /game — создание игры (action=None, game_id=None)
        if game_id is None and action is None:
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({
                    "error": "Request body must be a valid JSON object"
                }), 400

            dto = CreateGameRequestDTO.from_dict(data)
            if not dto:
                return jsonify({
                    "error": "Invalid game data format"
                }), 400

            player_id = g.current_user
            game_type = GameType.VSBOT if dto.type == "BOT" else (GameType.VSPLAYER if dto.type == "PLAYER" else None)
            if game_type is None:
                return jsonify({
                    "error": "Invalid game data format"
                }), 400
 
            
            game = self.game_service.create_game(player_id, game_type=game_type)
            return jsonify(WebGameMapper.to_web(game).to_dict()), 200


        else:
            try:
                game_uuid = UUID(game_id) 
            except (ValueError, TypeError):
                return jsonify({"error": "bad request"}), 400
            
            game = self.game_service.get_game(game_uuid)
            if game is None:
                return jsonify({"error": "game not found"}), 404

        # POST /game/<game_id>/join — присоединение (action="join")
            if action == "join":
                player_id = g.current_user

                result = self.game_service.join_game(game_uuid, player_id)
                if not result:
                    return jsonify({"error": "Conflict"}), 409

                return jsonify(WebGameMapper.to_web(result).to_dict())
                
        # POST /game/<game_id>/move — ход (action="move")
            elif action == "move":
                data = request.get_json(silent=True)
                if not data or not isinstance(data, dict):
                    return jsonify({
                        "error": "Request body must be a valid JSON object"
                    }), 400
                
                dto = MoveRequestDTO.from_dict(data)
                if not dto:
                    return jsonify({
                        "error": "Invalid move data format"
                    }), 400
                
                player_id = g.current_user

                result = self.game_service.make_move(game_id=game_uuid, player_id=player_id, row=dto.row, col=dto.col)
                if not result:
                    return jsonify({"error": "Invalid move: either previous moves were altered or more than one move was made"}), 422

                return jsonify(WebGameMapper.to_web(result).to_dict())

            else:
                return jsonify({"error": "page not found"}), 404

    def get(self, game_id: Optional[str] = None, action: Optional[str] = None):
        # GET /game — список доступных игр (game_id=None)
        if game_id is None and action is None:
            games = self.game_service.get_available_games()
            return jsonify([WebGameMapper.to_web(game).to_dict() for game in games]), 200

        # GET /game/<game_id> — получить историю игр (game_id="history")
        elif game_id == "history" and action is None:
            player_id = g.current_user
            games = self.game_service.get_finished_games(player_id)
            return jsonify([WebGameMapper.to_web(game).to_dict() for game in games]), 200

        # GET /game/liderboard/<n> — таблица лидеров
        elif game_id == 'liderboard' and action is not None and action.isdigit():
            int_action = int(action)

            if int_action <= 0: 
                return jsonify({"error": "bad request"}), 400
             
            liderboards = self.game_service.get_leaderboard(int_action)

            return jsonify([
                WebLiderBoardProfileMapper.to_web(liderboard).to_dict()
                for liderboard in liderboards
            ]), 200

        # GET /game/<game_id> — получить игру (game_id="...")
        else:
            try:
                game_uuid = UUID(game_id) 
            except (ValueError, TypeError):
                return jsonify({"error": "bad request"}), 400

            game = self.game_service.get_game(game_uuid)
            if game is not None:
                return jsonify(WebGameMapper.to_web(game).to_dict()), 200

        return jsonify({"error": "page not found"}), 404


     
def create_game_blueprint(game_service: IGameService):
    bp = Blueprint('game', __name__, url_prefix='/game')
    view = GameRoute.as_view('game_route', game_service=game_service)

    bp.add_url_rule('', view_func=view, methods=['GET', 'POST'])
    bp.add_url_rule('/<game_id>', view_func=view, methods=['GET'])
    bp.add_url_rule('/<game_id>/<action>', view_func=view, methods=['POST', 'GET'])

    return bp
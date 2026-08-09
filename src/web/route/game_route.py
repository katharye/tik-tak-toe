# web/route/game_route.py
from flask import Blueprint, jsonify, request
from flask.views import MethodView

from domain import GameServiceABC, Side
from web.mapper import WebGameMapper
from web.model import GameDTO

class GameRoute(MethodView):
    def __init__(self, game_service: GameServiceABC):
        super().__init__()
        self.game_service = game_service

    def post(self, game_id: str):
        data = request.get_json(silent=True)
        
        if not data or not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be a valid JSON object"
            }), 400
        
        game_dto = GameDTO.from_dict(data)
        if not game_dto:
            return jsonify({
                "error": "Invalid game data format"
            }), 400

        if game_id != game_dto.game_id:
            return jsonify({
                "error": "Invalid game UUID"
            }), 400

        game = WebGameMapper.to_domain(game_dto)
        if not self.game_service.validate_field(game):
            return jsonify ({
                "error": "Invalid move: either previous moves were altered or more than one move was made"
            }), 422

        is_over, winner = self.game_service.check_game_finish(game.board)
        if is_over:
            result = "draw" if winner == Side.CLEAR else ("player_wins" if winner == Side.PLAYER else "machine_wins")
            return jsonify({
                "game_id": str(game.uuid),
                "board": [row.copy() for row in game.board.values],
                "status": "finished",
                "result": result
            }), 200
        
        try:
            updated_game = self.game_service.get_next_move(game)

            is_over_after, winner_after = self.game_service.check_game_finish(updated_game.board)
            response = {
                "game_id": str(updated_game.uuid),
                "board": [row.copy() for row in updated_game.board.values],
                "status": "finished" if is_over_after else "ongoing"
            }
            if is_over_after:
                response["result"] = "draw" if winner_after == Side.CLEAR else (
                    "player_wins" if winner_after == Side.PLAYER else "machine_wins"
                )

            return jsonify(response), 200
            
        except Exception as e:
            return jsonify ({
                "error": str(e)
            }), 400
        
def create_game_blueprint(game_service: GameServiceABC):
    bp = Blueprint('game', __name__, url_prefix='/game')
    game_view = GameRoute.as_view('game_route', game_service=game_service)
    bp.add_url_rule('/<game_id>', view_func=game_view, methods=['POST'])
    return bp
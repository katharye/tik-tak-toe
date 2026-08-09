from flask import Blueprint, jsonify, request
from flask.views import MethodView
from base64 import b64decode 

from domain import IAuthService
from web.mapper import WebSignUpRequestMapper
from web.model import SignUpRequestDTO

class AuthRoute(MethodView):
    def __init__(self, auth_service: IAuthService):
        super().__init__()
        self.auth_service = auth_service

    def post(self, auth_method: str):
        if auth_method == "sign-up":
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({
                    "error": "Request body must be a valid JSON object"
                }), 400
        
            sign_up_request_dto = SignUpRequestDTO.from_dict(data)
            if not sign_up_request_dto:
                return jsonify({
                    "error": "Invalid sign up request format"
                }), 400

            sign_up_request_domain = WebSignUpRequestMapper.to_domain(sign_up_request_dto)
            result = self.auth_service.sign_up(sign_up_request_domain)

            if not result:
                return jsonify({
                    "error": "Conflict"
                }), 409

            return jsonify({"success": True}), 200
        
        elif auth_method == "sign-in":
            header = request.headers.get("Authorization")
            if header is None or not header.startswith("Basic "):
                return jsonify({
                    "error": "Request header must be a valid object"
                }), 400

            bytes_encoded = header.replace("Basic ", "", 1)
            decoded_str = b64decode(bytes_encoded).decode("utf-8")

            if ":" not in decoded_str:
                return jsonify({
                    "error": "Invalid format"
                }), 400
            
            login, password = decoded_str.split(":", 1)

            result = self.auth_service.sign_in(login, password)

            if result is not None:
                return jsonify({"user_id": str(result)}), 200

            return jsonify({
                "error": "Unauthorized"
            }), 401
            
        else:
            return jsonify({"error": "page not found"}), 404
        
def create_auth_blueprint(auth_service: IAuthService) -> Blueprint:
    bp = Blueprint('auth', __name__, url_prefix='/auth')

    auth_view = AuthRoute.as_view('auth_route', auth_service=auth_service)
    bp.add_url_rule('/<auth_method>', view_func=auth_view, methods=['POST'])

    return bp
from flask import Blueprint, jsonify, request
from flask.views import MethodView

from domain import IAuthService
from web.mapper import WebSignUpRequestMapper, WebJWTRequestMapper, WebJWTResponseMapper, WebJWTRefreshRequestMapper
from web.model import SignUpRequestDTO, JWTRequestDTO, JWTRefreshRequestDTO

class AuthRoute(MethodView):
    def __init__(self, auth_service: IAuthService):
        super().__init__()
        self.auth_service = auth_service

    def post(self, method: str):
        if method == "sign-up":
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
        
        elif method == "sign-in":
            data = request.get_json(silent=True)
            if data is None or not isinstance(data, dict):
                return jsonify({
                    "error": "Request body must be a valid object"
                }), 400


            request_dto = JWTRequestDTO.from_dict(data)
            if request_dto is None:
                return jsonify({
                    "error": "Invalid sign in request format"
                }), 400

            request_domain = WebJWTRequestMapper.to_domain(request_dto)

            response = self.auth_service.sign_in(request_domain)
            if response.access_token is None:
                return jsonify({"error": "Unauthorized"}), 401

            response_dto = WebJWTResponseMapper.to_web(response)

            return jsonify(response_dto.to_dict()), 200

        elif method in ("refresh-access", "refresh-refresh"):
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({
                    "error": "Request body must be a valid JSON object"
                }), 400

            refresh_request_dto = JWTRefreshRequestDTO.from_dict(data)
            if refresh_request_dto is None:
                return jsonify({"error": "Request body must be a valid JSON object"}), 400

            refresh_request = WebJWTRefreshRequestMapper.to_domain(refresh_request_dto)
            refresh_token = refresh_request.refresh_token

            result = None
            if method == "refresh-access":
                result = self.auth_service.refresh_access(refresh_token=refresh_token)
            elif method == "refresh-refresh":
                result = self.auth_service.refresh_refresh(refresh_token=refresh_token)

            response = WebJWTResponseMapper.to_web(result)
            if response.access_token != None or response.refresh_token != None:
                return jsonify(response.to_dict()), 200
            else:
                return jsonify({"error": "Unauthorized"}), 401  
            
        else:
            return jsonify({"error": "page not found"}), 404
        
def create_auth_blueprint(auth_service: IAuthService) -> Blueprint:
    bp = Blueprint('auth', __name__, url_prefix='/auth')

    auth_view = AuthRoute.as_view('auth_route', auth_service=auth_service)
    bp.add_url_rule('/<method>', view_func=auth_view, methods=['POST'])

    return bp
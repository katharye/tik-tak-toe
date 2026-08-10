from flask import Flask, Blueprint, jsonify, request, g
from uuid import UUID
from typing import Optional
from domain import IJWTProvider



class UserAuthenticator:
    def __init__(self, jwt_provider: IJWTProvider):
        self.jwt_provider = jwt_provider

    def authenticate(self) -> tuple[bool, Optional[UUID]]:
        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return (False, None)

        token = header.replace("Bearer ", "", 1)
        if self.jwt_provider.validate_access_token(token):
            user_id = self.jwt_provider.get_user_id(token)
            return (True, user_id)
        
        return (False, None)

    def register(self, app: Flask, exempt_blueprints: list[str]) -> None:
        self._exempt = exempt_blueprints
        @app.before_request
        def check_user():
            if request.blueprint in self._exempt:
                return None

            success, user_id = self.authenticate()
            if not success:
                return jsonify({"error": "Unauthorized"}), 401

            g.current_user = user_id

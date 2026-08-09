from flask import Flask, Blueprint, jsonify, request, g
from uuid import UUID
from typing import Optional
from domain import IAuthService

from base64 import b64decode 


class UserAuthenticator:
    def __init__(self, auth_service: IAuthService):
        self.auth_service = auth_service

    def authenticate(self) -> tuple[bool, Optional[UUID]]:
        header = request.headers.get("Authorization")
        if not header or not header.startswith("Basic "):
            return (False, None)

        bytes_encoded = header.replace("Basic ", "", 1)
        decoded_str = b64decode(bytes_encoded.encode("utf-8")).decode("utf-8")

        login, password = decoded_str.split(":", 1)

        result = self.auth_service.sign_in(login=login, password=password)
        if result is not None:
            return (True, result)
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

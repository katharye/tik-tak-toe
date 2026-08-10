from flask_jwt_extended import create_access_token, create_refresh_token, decode_token 

from uuid import UUID
from typing import Optional

from .jwt_provider_interface import IJWTProvider


class JWTProvider(IJWTProvider):

    def geterate_access_token(user_id: UUID) -> str: 
        return create_access_token(identity=str(user_id))

    def generate_refresh_token(user_id: UUID) -> str: 
        return create_refresh_token(identity=str(user_id))

    def validate_access_token(token: str) -> bool: 
        try:
            decoded_token = decode_token(token)

            if decoded_token.get("type", None) != "access":
                return False

            return True

        except Exception:
            return False

    def validate_refresh_token(token: str) -> bool: 
        try:
            decoded_token = decode_token(token)

            if decoded_token.get("type", None) != "refresh":
                return False

            return True

        except Exception:
            return False

    def get_user_id(token: str) -> Optional[UUID]: 
        try:
            decoded_token = decode_token(token)

            user_id = decoded_token.get("sub", None)

            if user_id is None:
                return None

            return UUID(str(user_id))

        except Exception:
            return None
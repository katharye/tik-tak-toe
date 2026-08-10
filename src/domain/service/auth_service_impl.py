from domain.interfaces import IPlayerRepository
from .auth_service_interface import IAuthService
from .jwt_provider_interface import IJWTProvider
from domain.model import Player, SignUpRequest, JWTResponse, JWTRequest


from uuid import uuid4, UUID
import hashlib

class AuthService(IAuthService):
    def __init__(self, player_repository: IPlayerRepository, jwt_provider: IJWTProvider):
        self.repository = player_repository
        self.jwt_provider = jwt_provider

    def sign_up(self, request: SignUpRequest) -> bool: 
        existing = self.repository.get_by_login(request.login)
        if existing:
            return False
        new_player = Player(
            player_id = uuid4(),
            login=request.login,
            password=self._hash(request.password)
        )
        self.repository.save(new_player)
        return True

    def sign_in(self, request: JWTRequest) -> JWTResponse: 
        existing = self.repository.get_by_login(request.login)
        if not existing:
            return JWTResponse(type="access", access_token=None, refresh_token=None)

        if not self._compare(db_password=existing.password, password=request.password):
            return JWTResponse(type="access", access_token=None, refresh_token=None)

        user_id = existing.player_id
        access_token = self.jwt_provider.generate_access_token(user_id)
        refresh_token = self.jwt_provider.generate_refresh_token(user_id)

        return JWTResponse(
            type="access",
            access_token=access_token,
            refresh_token=refresh_token
        )

    def refresh_access(self, refresh_token: str) -> JWTResponse: 
        if self.jwt_provider.validate_refresh_token(refresh_token):
            user_id = self.jwt_provider.get_user_id(refresh_token)
            if user_id is None:
                return JWTResponse(type="access", access_token=None, refresh_token=None)

            return JWTResponse(
                type="access",
                access_token=self.jwt_provider.generate_access_token(user_id),
                refresh_token=refresh_token
            )
        return JWTResponse(type="access", access_token=None, refresh_token=None)

    def refresh_refresh(self, refresh_token: str) -> JWTResponse: 
        if self.jwt_provider.validate_refresh_token(refresh_token):
            user_id = self.jwt_provider.get_user_id(refresh_token)
            if user_id is None:
                return JWTResponse(type="refresh", access_token=None, refresh_token=None)
            return JWTResponse(
                type="refresh",
                access_token=None,
                refresh_token=self.jwt_provider.generate_refresh_token(user_id)
            )
        return JWTResponse(type="refresh", access_token=None, refresh_token=None)


    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _compare(self, db_password, password):
        return db_password == self._hash(password)

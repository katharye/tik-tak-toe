from domain.interfaces import IPlayerRepository
from domain.service.auth_service_interface import IAuthService
from domain.model import Player, SignUpRequest

from uuid import uuid4, UUID
import hashlib

class AuthService(IAuthService):
    def __init__(self, player_repository: IPlayerRepository):
        self.repository = player_repository

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

    def sign_in(self, login: str, password: str) -> UUID | None:
        existing = self.repository.get_by_login(login)
        if not existing:
            return None

        if not self._compare(db_password=existing.password, password=password):
            return None

        return existing.player_id


    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _compare(self, db_password, password):
        return db_password == self._hash(password)

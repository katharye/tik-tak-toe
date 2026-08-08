from domain.model import SignUpRequest

from abc import ABC, abstractmethod
from uuid import UUID

class IAuthService(ABC):

    @abstractmethod
    def sign_up(self, request: SignUpRequest) -> bool: ...

    @abstractmethod
    def sign_in(self, login: str, password: str) -> UUID | None: ...
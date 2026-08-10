from domain.model import SignUpRequest, JWTRequest, JWTResponce


from abc import ABC, abstractmethod
from uuid import UUID

class IAuthService(ABC):

    @abstractmethod
    def sign_up(self, request: SignUpRequest) -> bool: ...

    @abstractmethod
    def sign_in(self, request: JWTRequest) -> JWTResponce: ...

    @abstractmethod
    def refresh_access(self, refresh_token: str) -> JWTResponce: ...

    @abstractmethod
    def refresh_refresh(self, refresh_token: str) -> JWTResponce: ...
    
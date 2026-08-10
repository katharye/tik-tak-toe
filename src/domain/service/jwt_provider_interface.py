from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

class IJWTProvider(ABC):

    @abstractmethod
    def generate_access_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def generate_refresh_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def validate_access_token(self, token: str) -> bool: ...

    @abstractmethod
    def validate_refresh_token(self, token: str) -> bool: ...

    @abstractmethod
    def get_user_id(self, token: str) -> Optional[UUID]: ...
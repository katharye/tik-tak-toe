from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

class IJWTProvider(ABC):

    @classmethod
    @abstractmethod
    def geterate_access_token(user_id: UUID) -> str: ...

    @classmethod
    @abstractmethod
    def generate_refresh_token(user_id: UUID) -> str: ...

    @classmethod
    @abstractmethod
    def validate_access_token(token: str) -> bool: ...

    @classmethod
    @abstractmethod
    def validate_refresh_token(token: str) -> bool: ...

    @classmethod
    @abstractmethod
    def get_user_id(token: str) -> Optional[UUID]: ...
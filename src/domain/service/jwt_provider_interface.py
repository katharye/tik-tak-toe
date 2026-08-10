from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

class IJWTProvider(ABC):

    @abstractmethod
    def geterate_access_token(user_id: UUID) -> str: ...

    @abstractmethod
    def generate_refresh_token(user_id: UUID) -> str: ...

    @abstractmethod
    def validate_access_token(token: str) -> bool: ...

    @abstractmethod
    def validate_refresh_token(token: str) -> bool: ...

    @abstractmethod
    def get_user_id(token: str) -> Optional[UUID]: ...
# web/model/board_dto.py
from typing import Self, Optional
from dataclasses import dataclass

@dataclass
class PlayerDTO:
    id: str
    login: str
    password: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "login": self.login,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        id = data.get("id")
        login = data.get("login")
        password = data.get("password")
        if None in (id, login, password):
            return None
        
        return PlayerDTO(
            id=id, 
            login=login,
            password=password
        )
    
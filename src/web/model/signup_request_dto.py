# web/model/board_dto.py
from typing import Self, Optional
from dataclasses import dataclass

@dataclass
class SignUpRequestDTO:
    login: str
    password: str

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "player_password256": self.password
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        login = data.get("login")
        password = data.get("password")
        if login is None or password  is None:
            return None
        
        return SignUpRequestDTO(
            login=login, 
            password=password
        )

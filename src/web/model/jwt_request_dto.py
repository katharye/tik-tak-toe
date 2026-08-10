from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class JWTRequestDTO:
    login: str
    password: str

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        login = data.get("login", None)
        password = data.get("password", None)
        if None not in (login, password):
            return JWTRequestDTO(login=login, password=password)    
                        
        return None
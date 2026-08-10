from dataclasses import dataclass

@dataclass
class JWTRequest:
    login: str
    password: str
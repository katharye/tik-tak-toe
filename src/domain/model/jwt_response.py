from dataclasses import dataclass

@dataclass
class JWTResponce:
    type: str
    access_token: str
    refresh_token: str
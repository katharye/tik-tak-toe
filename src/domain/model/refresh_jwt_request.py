from dataclasses import dataclass

@dataclass
class JWTRefreshRequest:
    refresh_token: str
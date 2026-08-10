from dataclasses import dataclass

@dataclass
class JWTRefreshRequest:
    refresh_tocken: str
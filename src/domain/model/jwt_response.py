from dataclasses import dataclass
from typing import Optional

@dataclass
class JWTResponce:
    type: str
    access_token: Optional[str]
    refresh_token: Optional[str]
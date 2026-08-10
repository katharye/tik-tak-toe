from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class JWTRefreshRequestDTO:
    refresh_token: str

    def to_dict(self) -> dict:
        return {
            "refresh_token": self.refresh_token,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        refresh_token = data.get("refresh_token", None)
        if refresh_token is not None:
            return JWTRefreshRequestDTO(refresh_token=refresh_token)    
                        
        return None
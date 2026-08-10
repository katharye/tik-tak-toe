from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class JWTRefreshRequestDTO:
    refresh_tocken: str

    def to_dict(self) -> dict:
        return {
            "refresh_tocken": self.refresh_tocken,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        refresh_tocken = data.get("refresh_tocken", None)
        if refresh_tocken is not None:
            return JWTRefreshRequestDTO(refresh_tocken=refresh_tocken)    
                        
        return None
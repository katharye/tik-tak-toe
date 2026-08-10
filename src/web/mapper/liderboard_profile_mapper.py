from domain import LiderBoardProfile
from web.model import LiderBoardProfileDTO

class WebLiderBoardProfileMapper:

    @classmethod
    def to_web(cls, domain: LiderBoardProfile) -> LiderBoardProfileDTO: 
        return LiderBoardProfileDTO(
            player_id=str(domain.player_id),
            login=domain.login,
            win_ratio=domain.win_ratio,
        )
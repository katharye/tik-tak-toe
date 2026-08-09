from domain import Player
from web.model import PlayerDTO

from uuid import UUID

class WebPlayerMapper:

    @classmethod
    def to_web(cls, domain: Player) -> PlayerDTO: 
        return PlayerDTO(
            id=str(domain.player_id),
            login=str(domain.login),
        )

    @classmethod
    def to_domain(cls, web: PlayerDTO) -> Player: 
        return Player (
            player_id=UUID(web.id),
            login=web.login,
            password=web.password
        )
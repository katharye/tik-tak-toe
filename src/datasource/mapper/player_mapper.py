from uuid import UUID
from datasource.model import PlayerEntity
from domain import Player

class DatasourcePlayerMapper:

    @classmethod
    def to_domain(cls, entity: PlayerEntity) -> Player:
        return Player(
            player_id=UUID(entity.player_id),
            login=entity.player_login,
            password=entity.player_password
        )

    @classmethod
    def to_data(cls, domain: Player) -> PlayerEntity:
        return PlayerEntity(
            player_id=str(domain.player_id),
            player_login=domain.login,
            player_password=domain.password
        )
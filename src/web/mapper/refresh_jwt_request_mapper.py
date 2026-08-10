from domain import JWTRefreshRequest
from web.model import JWTRefreshRequestDTO

class WebJWTRefreshRequestMapper:

    @classmethod
    def to_web(cls, domain: JWTRefreshRequest) -> JWTRefreshRequestDTO: 
        return JWTRefreshRequestDTO(
            refresh_token=domain.refresh_token
        )

    @classmethod
    def to_domain(cls, web: JWTRefreshRequestDTO) -> JWTRefreshRequest: 
        return JWTRefreshRequest (
            refresh_token=web.refresh_token
        )
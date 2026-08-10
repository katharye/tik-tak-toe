from domain import JWTResponse
from web.model import JWTResponseDTO

class WebJWTResponseMapper:

    @classmethod
    def to_web(cls, domain: JWTResponse) -> JWTResponseDTO: 
        return JWTResponseDTO(
            type=domain.type,
            access_token=domain.access_token,
            refresh_token=domain.refresh_token
        )

    @classmethod
    def to_domain(cls, web: JWTResponseDTO) -> JWTResponse: 
        return JWTResponse (
            type=web.type,
            access_token=web.access_token,
            refresh_token=web.refresh_token
        )
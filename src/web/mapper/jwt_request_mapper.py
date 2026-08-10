from domain import JWTRequest
from web.model import JWTRequestDTO

class WebJWTRequestMapper:

    @classmethod
    def to_web(cls, domain: JWTRequest) -> JWTRequestDTO: 
        return JWTRequestDTO(
            login=domain.login,
            password=domain.password
        )

    @classmethod
    def to_domain(cls, web: JWTRequestDTO) -> JWTRequest: 
        return JWTRequest (
            login=web.login,
            password=web.password
        )
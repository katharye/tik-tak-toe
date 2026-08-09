from domain import SignUpRequest
from web.model import SignUpRequestDTO

from uuid import UUID

class WebSignUpRequestMapper:

    @classmethod
    def to_web(cls, domain: SignUpRequest) -> SignUpRequestDTO: 
        return SignUpRequestDTO(
            login=domain.login,
            password=domain.password
        )

    @classmethod
    def to_domain(cls, web: SignUpRequestDTO) -> SignUpRequest: 
        return SignUpRequest (
            login=web.login,
            password=web.password
        )
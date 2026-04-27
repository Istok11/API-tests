import requests

from .base_client import BaseClient
from ..models.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse


class AuthClient(BaseClient):
    def __init__(self, base_url: str, token: str | None = None):
        super().__init__(base_url)
        self.token = token

    # -------- LOW LEVEL lOGIN ---------
    def login(self, request: LoginRequest) -> LoginResponse:
        response = self.post(
            "/api/auth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=request.model_dump(),
        )
        assert response.status_code == 200, response.text
        result = LoginResponse(**response.json())

        self.token = result.access_token

        self.session.headers.update({
            "Authorization": f"Bearer {result.access_token}",
        })

        return result



    def register(self, request: RegisterRequest) -> RegisterResponse:
        response = self.post(
            "/api/auth/register",
            json=request.model_dump()
        )

        assert response.status_code == 200, response.text
        return RegisterResponse(**response.json())

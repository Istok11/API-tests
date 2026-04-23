import requests

from .base_client import BaseClient
from ..models.users import UsersResponse


class UsersClient(BaseClient):
    def get_me(self) -> UsersResponse:
        response = self.get("/api/users/me")

        assert response.status_code == 200, response.text

        return UsersResponse(**response.json())
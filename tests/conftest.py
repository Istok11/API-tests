import os
import pytest
from dotenv import load_dotenv

from src.clients.auth_client import AuthClient
from src.clients.issues_client import IssueClient
from src.clients.users_client import UsersClient
from src.models.auth import LoginRequest

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")


@pytest.fixture(scope="session")
def auth_client(base_url) -> AuthClient:
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    assert login is not None, "LOGIN not set in .env"
    assert password is not None, "PASSWORD not set in .env"

    client = AuthClient(base_url)

    request = LoginRequest(
        username=login,
        password=password
    )

    client.login(request)

    return client


@pytest.fixture
def issue_client(auth_client) -> IssueClient:
    return IssueClient(
        base_url=auth_client.base_url,
        session=auth_client.session
    )


@pytest.fixture
def users_client(auth_client) -> UsersClient:
    return UsersClient(
        base_url=auth_client.base_url,
        session=auth_client.session
    )
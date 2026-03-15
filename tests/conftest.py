import os
import requests
import pytest
from dotenv import load_dotenv
load_dotenv()



@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")

@pytest.fixture(scope="session")
def access_token(base_url):
    response = requests.post(
        f"{base_url}/api/auth/token",
        headers = {"Content-Type": "application/x-www-form-urlencoded"},
        data = {
            "grant_type": "",
            "username": os.getenv("LOGIN"),
            "password": os.getenv("PASSWORD"),
            "scope": "",
            "client_id": "string",
            "client_secret": "********",
        },
        timeout=10,
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

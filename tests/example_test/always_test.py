
import requests
import os
import json



def test_get_users_me(access_token, base_url):

    response = requests.get(
        f"{base_url}/api/users/me",
        headers={"Authorization": f"Bearer {access_token}", "accept": "application/json"},
        timeout=10,
    )
    assert response.status_code == 200, response.text

    print(response.json())

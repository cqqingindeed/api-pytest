# import requests
from clients.api_client import APIClient

from configs.settings import BASE_URL
import pytest

api_client = APIClient()

@pytest.mark.AUTH("001")
def test_verify_user_can_login_with_valid_credentials():
        # make the call
    # url = f"{BASE_URL}/api/v1/auth/login"
    endpoint = f"/api/v1/auth/login"
    # breakpoint()
    payload = {"email": "student@example.com", "password": "Password123!"}
    # api_client = APIClient()
    # response = requests.post(url, json=payload)
    # breakpoint()
    # verify response code
    # assert response.status_code == 200
    # verify the body
    # response_body = response.json()
    # response_body = requests.post_json(url, json=payload)
    response_body = api_client.post_json(endpoint, payload)
    # breakpoint()
    assert response_body["access_token"]
    assert response_body["token_type"] == "bearer"
    assert response_body["user"]["email"] == payload["email"]
    # more assert


@pytest.mark.AUTH("002")
def test_verify_user_cannot_login_with_invalid_credential():
    endpoint = f"/api/v1/auth/login"
    # header = 
    payload = {"email": "student@example.com", "password": "wrongpassword"}

    # api_client = APIClient()
    # response = requests.post(url, json=payload)
    response_body = api_client.post_json(endpoint, payload, None, 401)
    # breakpoint()
    # assert response_body.status_code == 401
    assert response_body["error"]["code"] == "INVALID_CREDENTIALS"
    assert response_body["error"]["message"] == "Invalid email or password"

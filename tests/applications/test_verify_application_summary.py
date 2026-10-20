#import requests
from clients.api_client import APIClient
# from configs.settings import BASE_URL
from helpers.auth_helper import login_user
import pytest


@pytest.mark.APPS("002")
def test_verify_authenticated_user_can_get_applications_summary():
    # get JWT token.
    # login with user and get the token
    # url = f"{BASE_URL}/api/v1/auth/login"
    # # header = 
    # payload = {"email": "student@example.com", "password": "Password123!"}
    # response = requests.post(url, json=payload)   
    # assert response.status_code == 200
    # # make the api call with token
    # access_token = response.json()["access_token"]
    # access_token = login_user() # comment out this after adding headers in api_client
    # headers = {"Authorization": f"Bearer {access_token}"}

    endpoint =  f"/api/v1/applications/summary"
    # response = requests.get(url, headers=headers)
    api_client = APIClient()
    response_body = api_client.get_json(endpoint) #, headers=headers)
    # assert response.status_code == 200
    # breakpoint()
    # response_body = response.json()
    assert response_body, "response body is not empty"
    assert isinstance(response_body["potential"], int)
    # add more assert



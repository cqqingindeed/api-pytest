# import requests
from clients.api_client import APIClient    # this replace import requests
# from configs.settings import BASE_URL
from helpers.auth_helper import login_user


def test_verify_authenticated_user_get_applications():
    # get JWT token.
    # login with user and get the token
    # url = f"{BASE_URL}/api/v1/auth/login"
    # # header = 
    # payload = {"email": "student@example.com", "password": "Password123!"}
    # response = requests.post(url, json=payload)   
    # # make the api call with token
    # access_token = response.json()["access_token"]

    # access_token = login_user()
    # breakpoint()
    # headers = {"Authorization": f"Bearer {access_token}"}
    # breakpoint()
    endpoint = f"/api/v1/applications"

    api_client = APIClient()
    # response = api_client.get(get_application_url, headers=headers)
    # response = api_client.get_json(get_application_url, headers=headers)
    # response = requests.get(get_application_url, headers=headers)

    # breakpoint()
    # assert response.status_code == 200 #comment out. it was checked in api_client 
    # verify the body
    # response_body = response.json()
    response_body = api_client.get_json(endpoint) #, headers=headers)
    assert isinstance(response_body, list)
    assert response_body

    # verify api call 
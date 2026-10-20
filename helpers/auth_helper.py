from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD
# import requests
from clients.api_client import APIClient

def login_user(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
    url = f"{BASE_URL}/api/v1/auth/login"
    endpoint = f"/api/v1/auth/login"
    # header = 
    payload = {"email": email, "password": password}

    api_client = APIClient()
    # response = requests.post(url, json=payload)   
    # assert response.status_code == 200
    #response_body = requests.post_json(url, json=payload)
    # breakpoint() 
    response_body = api_client.post_json(endpoint, payload)
    # make the api call with token
    access_token = response_body["access_token"]
    return access_token
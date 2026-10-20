# import requests
from clients.api_client import APIClient
import pytest
# from configs.settings import BASE_URL

@pytest.mark.PUBLIC("001")
def test_verify_public_status_endpoint():
    # make the call
    endpoint = f"/api/v1/public/status"
    api_client = APIClient()
    # response = requests.get(url)
    # # verify status code
    # status_code = response.status_code
    # assert status_code == 200, "verify status code is 200"
    # #verity the body
    # response_body = response.json()
    response_body = api_client.get_json(endpoint) #, None)
    # breakpoint()    # this is replacement for pdb. 
    assert response_body["app_name"] == "SuperSQA Job Tracker"
    assert response_body["environment"] == "local"
    assert response_body["api_version"] == "v1"
    assert response_body["server_time"], "verify server time exists"
    print("this is my first test ")

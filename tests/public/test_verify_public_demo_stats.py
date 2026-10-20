import requests
from clients.api_client import APIClient
import pytest
# from configs.settings import BASE_URL

@pytest.mark.PUBLIC("002")
def test_verify_public_demo_stats():
    # make the call
    endpoint = f"/api/v1/public/demo-stats"
    api_client = APIClient()
    # response = requests.get(url)
    # verify status code
    # status_code = response.status_code
    # assert status_code == 200, "verify status code is 200"

    # verity the body
    # response_body = response.json()
    response_body = api_client.get_json(endpoint) #, None)
    # verity there are 2 keys in the response body
    assert len(response_body.keys()) == 2, "verity there are 2 keys"
    assert isinstance(response_body["total_seeded_applications"], int), "verify response body is a integer"
    assert isinstance(response_body["status_counts"], dict), "verify response body is a dict"
    status_counts = response_body["status_counts"]
    for k, v in status_counts.items():
        # assert isinstance(k, str), "verify key is a string"
        assert isinstance(v, int), "verify value is a integer"

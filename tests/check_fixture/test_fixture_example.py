import pytest
from clients.api_client import APIClient


def test_fixture_sheng(sheng):
    print("this is in test_fixture_example")


def test_get_api_client(api_client):
    # api_client = APIClient()
    resp_json = api_client.get_json("/api/v1/applications")
    assert resp_json
    assert "company_name" in resp_json[0]


def test_verify_all_modifyitems(unauthenticated_api_client):
    resp = unauthenticated_api_client.get_json("/api/v1/applications", expected_status_code=401)
    assert resp["error"]
    assert resp["error"]["message"] == "Authentication required"


def test_verify_create_then_delete(create_application_fixture):
    resp = create_application_fixture
    breakpoint()
    print("back to fixture due to the yield - ")
    

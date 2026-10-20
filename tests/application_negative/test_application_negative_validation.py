from helpers.application_helper import build_create_applicaiton_payload, create_application, get_application
from clients.api_client import APIClient
from helpers.error_helper import verify_error_response
import pytest

# api_client = APIClient()

@pytest.mark.APPNEG("001")
def test_verify_create_application_requesed_company_name():
    #prepare payload without company name
    api_client = APIClient()
    payload = build_create_applicaiton_payload()
    payload.pop("company_name")

    resp = create_application(api_client, payload, 422)
    # breakpoint()
    assert "error" in resp.keys(), f"Verify error key"
    assert resp["error"]["code"] == "VALIDATION_ERROR"
    assert resp["error"]["details"]
    assert resp["error"]["details"][0]["loc"][1] == "company_name"
    assert resp["error"]["details"][0]["type"] == "missing"


@pytest.mark.APPNEG("002")
def test_verify_create_application_reject_invalid_status():
    #prepare payload without company name
    api_client = APIClient()
    payload = build_create_applicaiton_payload(status="invalid_status")
    
    resp = create_application(api_client, payload, 422)
    # breakpoint()
    assert "error" in resp.keys(), f"Verify error key"
    assert resp["error"]["code"] == "VALIDATION_ERROR"
    assert resp["error"]["details"]
    assert resp["error"]["details"][0]["loc"][1] == "status"
    assert resp["error"]["details"][0]["type"] == "enum"


@pytest.mark.APPNEG("003")
def test_verify_noneexistent_application_return_not_found():
    #prepare payload without company name
    api_client = APIClient()
    application_id = 99999999
    resp = get_application(api_client, application_id, expected_status_code=404)
    # assert resp["error"]["code"] == "NOT_FOUND"
    # assert resp["error"]["message"] == "Application not found"
    verify_error_response(resp, "NOT_FOUND", "Application not found")


@pytest.mark.APPNEG("004")
def test_verify_application_list_request_authentication():
    # make get call without authentication
    get_application_endpoint = "/api/v1/applications"

    api_client = APIClient(authenticated=False)
    resp = resp = api_client.get_json(get_application_endpoint, expected_status_code=401)
    # breakpoint()
    verify_error_response(resp, "AUTHENTICATION_REQUIRED", "Authentication required")

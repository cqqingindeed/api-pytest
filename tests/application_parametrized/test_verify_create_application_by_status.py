from clients.api_client import APIClient
from helpers.application_helper import build_create_applicaiton_payload, create_application, delete_application
import pytest


@pytest.mark.parametrize("exp_status, title", [("potential", "SQA"), ("applied", "SQLDev"), ("in_progress","DBAdmin")])
def test_verify_user_can_create_applicaiton_with_status(exp_status, title):
    api_client = APIClient()
    # expected_status = "potential"
    payload = build_create_applicaiton_payload(status=exp_status, role_title=title)
    try:
        response = create_application(api_client, payload=payload)
        application_id = response["id"]
        assert response["company_name"] == payload["company_name"]
        assert response["status"] == exp_status
        assert response["role_title"] == title 
    finally:
        delete_application(api_client, application_id)




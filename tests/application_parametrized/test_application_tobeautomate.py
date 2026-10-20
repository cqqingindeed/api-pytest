import pytest

from clients.api_client import APIClient
from helpers.application_helper import build_create_applicaiton_payload, create_application


@pytest.mark.parametrize(
    ("test_case_id", "field", "value", "expected_error_type"),
    [
        pytest.param("APPNEG-CREATE-001", "company_name", None, "missing", id="missing-company-name"),
        pytest.param("APPNEG-CREATE-002", "role_title", None, "missing", id="missing-role-title"),
        pytest.param("APPNEG-CREATE-003", "status", "invalid_status", "enum", id="invalid-status"),
        pytest.param(
            "APPNEG-CREATE-004",
            "remote_type",
            "invalid_remote_type",
            "enum",
            id="invalid-remote-type",
        ),
    ],
)
def test_verify_create_application_rejects_invalid_payload(
    test_case_id, field, value, expected_error_type
):
    """Cover the negative application-creation cases in application-tobeautomate.csv."""
    api_client = APIClient()
    payload = build_create_applicaiton_payload()

    if value is None:
        payload.pop(field)
    else:
        payload[field] = value

    response = create_application(api_client, payload, expected_status_code=422)

    assert response["error"]["code"] == "VALIDATION_ERROR", test_case_id
    assert response["error"]["details"], test_case_id
    assert any(
        detail["loc"][-1] == field and detail["type"] == expected_error_type
        for detail in response["error"]["details"]
    ), test_case_id

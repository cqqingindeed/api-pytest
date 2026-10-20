from helpers.application_helper import create_application, get_application, delete_application
from helpers.application_helper import build_create_applicaiton_payload
from clients.api_client import APIClient
import pytest

api_client = APIClient()
@pytest.mark.APPS("006")
def test_verify_user_can_update_application_nodes():
    # setup: api call and create app
    # api_client = APIClient()
    # create a payload
    application_info = create_application(api_client)
    application_id = application_info["id"]
    note_before = application_info["notes"]
    # breakpoint()
    # update
    update_endpoint = f"/api/v1/applications/{application_id}"
    # only update nodes
    payload = {"notes": "API Automation Testing"}
    update_response = api_client.patch_json(update_endpoint, data=payload)
    assert update_response["notes"] == payload["notes"]

    get_application_info = get_application(api_client, application_id)
    assert get_application_info["notes"] == payload["notes"]
    
    # delete application
    delete_application(api_client, application_id)

@pytest.mark.APPS("007")
def test_verify_user_can_update_application_remote_type():
    old_remote_type = "on_site"
    new_remote_type = "hybrid"
    payload = build_create_applicaiton_payload(remote_type=old_remote_type)
    # payload.update({"remote_type": old_remote_type})
    # breakpoint()
    application_info = create_application(api_client, payload)
    application_id = application_info["id"]
    # update remote_type = "hybrid"
    # payload.update({"remote_type": new_remote_type})
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {"remote_type": new_remote_type}
    update_response = api_client.patch_json(update_endpoint, data=update_payload)
    # breakpoint()
    assert update_response["remote_type"] == new_remote_type

    get_app_info = get_application(api_client, application_id)
    assert get_app_info["remote_type"] == new_remote_type

    delete_application(api_client, application_id)


@pytest.mark.APPS("008")
def test_verify_user_can_update_application_salary_range():
    old_salary_range = "$100k - $130k"
    new_salary_range = "$150k - $180k"
    payload = build_create_applicaiton_payload(salary_range=old_salary_range)
    # payload.update({"remote_type": old_remote_type})
    # breakpoint()
    application_info = create_application(api_client, payload)
    application_id = application_info["id"]
    # update remote_type = "hybrid"
    # payload.update({"remote_type": new_remote_type})
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {"salary_range": new_salary_range}
    update_response = api_client.patch_json(update_endpoint, data=update_payload)
    # breakpoint()
    assert update_response["salary_range"] == new_salary_range

    get_app_info = get_application(api_client, application_id)
    assert get_app_info["salary_range"] == new_salary_range

    delete_application(api_client, application_id)


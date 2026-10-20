from clients.api_client import APIClient
import pytest

@pytest.mark.APPS("003")
def test_verify_user_can_create_application():

    # create a payload
    payload = {"company_name": "SuperSQA",
                "job_url": "https://superqa.com/jobs/api-test-engineer",
                "location": "Remote",
                "next_action": "Follow up with recruiter",
                "notes": "Submitted through company careers page.",
                "remote_type": "remote",
                "role_title": "API Test Engineer",
                "salary_range": "$170k - $200k",
                "status": "applied"
            }
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, None, 201)
    # breakpoint()
    # make a api call

    # verify the response
    assert isinstance(create_application_json["id"], int), "id is int"
    assert create_application_json["company_name"] == payload["company_name"]
    assert create_application_json["description"] == None, "description is null"
    # add more assert

    # do a get call and verify the item being created
    endpoint = f'/api/v1/applications/{create_application_json["id"]}'
    response_json = api_client.get_json(endpoint)
    # breakpoint()
    assert response_json
    assert response_json["company_name"] == payload["company_name"]
    # add more assert 

    # clean up / teardown - delete app being created
    id = create_application_json["id"]
    delete_endpoint = f"/api/v1/applications/{id}"
    response = api_client.delete(delete_endpoint)


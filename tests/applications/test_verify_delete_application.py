from clients.api_client import APIClient


def test_verify_user_can_delete_application():
    # create an application
    payload = {"company_name": "SuperSQA-ToBeDeleted",
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
    # verify the application was created successfully
        # do a get call and verify the item being created
    endpoint = f'/api/v1/applications/{create_application_json["id"]}'
    response_json = api_client.get_json(endpoint)
    # breakpoint()
    assert response_json
    assert response_json["company_name"] == payload["company_name"]

    # delete application
    id = create_application_json["id"]
    delete_endpoint = f"/api/v1/applications/{id}"
    response_delete = api_client.delete(delete_endpoint) # status code 204 was verified 
    # breakpoint()

    # verify deleted - search the deleted application
    get_endpoint = f"/api/v1/applications/{create_application_json["id"]}"
    response_json = api_client.get(get_endpoint, expected_status_code=404)
    # breakpoint()
    # assert response_json
    # assert response_json["company_name"] == payload["company_name"]




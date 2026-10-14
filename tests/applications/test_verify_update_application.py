from clients.api_client import APIClient

def test_verify_user_can_update_application():
    # setup - create a new ap[lication
    # create a payload
    payload = {"company_name": "SuperSQA1",
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
    assert isinstance(create_application_json["id"], int), "id is int"
    assert create_application_json["company_name"] == payload["company_name"]

    # test - update the application
    id = create_application_json["id"]
    endpoint = f"/api/v1/applications/{id}"
    # breakpoint()
    payload = {"next_action": "update next action",
            "notes": "Recruiter screen completed.",
            "status": "hired"
        }
    
    patch_json_response = api_client.patch_json(endpoint, data=payload)
    # breakpoint()
    assert patch_json_response["status"] == payload["status"]
    assert patch_json_response["id"] == id, "Make sure the specific one is updated" 


    #teardown - delete application
    # id = create_application_json["id"]
    delete_endpoint = f"/api/v1/applications/{id}"
    response = api_client.delete(delete_endpoint)

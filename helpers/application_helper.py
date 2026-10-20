# from clients.api_client import APIClient


def create_application(api_client, payload=None, expected_status_code=201):
    # create a payload
    if not payload:
        payload = build_create_applicaiton_payload()
    endpoint = "/api/v1/applications"
    # api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, None, expected_status_code) #201)
    return create_application_json
 

def build_create_applicaiton_payload(**overrides):
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
    payload.update(overrides)
    return payload

def get_application(api_client, application_id, expected_status_code=200):
    get_application_endpoint = f"/api/v1/applications/{application_id}"
    return api_client.get_json(get_application_endpoint, expected_status_code=expected_status_code)


def delete_application(api_client, application_id):
    delete_application_endpoint = f"/api/v1/applications/{application_id}"
    api_client.delete(delete_application_endpoint)




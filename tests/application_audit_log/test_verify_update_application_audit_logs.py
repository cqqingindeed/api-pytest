from clients.api_client import APIClient
from clients.sql_client import SQLClient
import pytest

@pytest.mark.AUDIT("003")
def test_verify_create_applicaiton_writes_to_audot_log_V2():
    # same case but using SQLClient
    status_before = "potential"
    status_after = "applied"
    payload = {"company_name": "SuperSQA",
                "job_url": "https://superqa.com/jobs/api-test-engineer",
                "location": "Remote",
                "next_action": "Follow up with recruiter",
                "notes": "Submitted through company careers page.",
                "remote_type": "remote",
                "role_title": "API Test Engineer",
                "salary_range": "$170k - $200k",
                "status": status_before
            }
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, None, 201)
    #verify the log table
    application_id = create_application_json["id"]
    # make api call to update
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_data = {"status": status_after}
    api_client.patch(update_endpoint, update_data)

    sql = f"""SELECT * FROM application_audit_logs WHERE created_at >= datetime('now', '-2 minute');"""
 
    sql_client = SQLClient() #DATABASE_PATH)
    audit_log = sql_client.execute_query(sql)
    # breakpoint()
    lis = [status_before, status_after]
    for item in audit_log:
        if item["old_status"] == status_before:
            assert item["new_status"] == status_after

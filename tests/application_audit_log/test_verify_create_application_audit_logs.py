from clients.api_client import APIClient
import sqlite3
from clients.sql_client import SQLClient
# from configs.setting.py import DATABASE_PATH
# from pathlib import Path
import pytest


@pytest.mark.AUDIT("001")
def test_verify_create_applicaiton_writes_to_audot_log():
    # make applicaiton cal - create app
    # helps.create_application()
    # create a applicaiton
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
    #verify the log table
    application_id = create_application_json["id"]
    # breakpoint()
    #c create connection
    DATABASE_PATH = "/Users/schen/api-testing/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db"
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    sql = f"""SELECT * FROM application_audit_logs WHERE created_at >= datetime('now', '-3 minute');"""
    cursor.execute(sql)
    audit_log = cursor.fetchone()  # this will fetch one row
    cursor.close()
    connection.close() 
    # breakpoint()
    assert audit_log, f"Expected row in audit log for app id:{application_id}"
    # assert audit_log["application_id"] == application_id
    assert audit_log["action"] == "created"
    assert audit_log["user_id"] 
    assert audit_log["old_status"] is None


@pytest.mark.AUDIT("002")
def test_verify_create_applicaiton_writes_to_audot_log_V2():
    # same case but using SQLClient
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
    #verify the log table
    application_id = create_application_json["id"]
    # DATABASE_PATH = "/Users/schen/api-testing/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db"

    sql = f"""SELECT * FROM application_audit_logs WHERE created_at >= datetime('now', '-3 minute');"""
 
    sql_client = SQLClient() #DATABASE_PATH)
    audit_log = sql_client.execute_query(sql)
    assert audit_log[0], f"Expected row in audit log for app id:{application_id}"
    #assert audit_log[0]["application_id"] == application_id
    assert audit_log[0]["action"] == "created"
    assert audit_log[0]["user_id"] 
    assert audit_log[0]["old_status"] is None
    # breakpoint()
    # for row in audit_log:
    #     assert row, f"Expected row in audit log for app id:{application_id}"
    #     assert row["application_id"] == application_id
    #     assert row["action"] == "created"
    #     assert row["user_id"] 
    #     assert row["old_status"] is None
    #

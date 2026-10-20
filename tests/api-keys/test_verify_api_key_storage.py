from clients.api_client import APIClient
from clients.sql_client import SQLClient
import pytest

@pytest.mark.APIKEY("001")
def test_verify_api_key_is_not_stored_as_plain_text():
    api_client = APIClient()
    # make a call to create a new api key
    create_api_key_endpoint = "/api/v1/api-keys"
    create_api_key_payload = {"name": "API Testing Automation"}
    create_key_json = api_client.post_json(create_api_key_endpoint, create_api_key_payload, expected_status_code=201)
    # breakpoint()
    api_key = create_key_json["api_key"]
    key_prefix = create_key_json["key_prefix"]
    key_id = create_key_json["id"]
    # assert api_key.startswith("jt_live_")
    # assert key_prefix.startswith("jt_live_")
    assert api_key.startswith(key_prefix)

    # verify in DB
    sql = f"select hashed_key, key_prefix from api_keys where id = {key_id}"
    sql_client = SQLClient()
    db_row = sql_client.execute_query(sql)
    # breakpoint()
    assert db_row[0]["key_prefix"] == key_prefix
    assert db_row[0]["hashed_key"] != api_key

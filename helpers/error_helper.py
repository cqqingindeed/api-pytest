

def verify_error_response(response_json, expected_code, expected_message):
    assert response_json["error"]
    assert response_json["error"]["code"] == expected_code
    assert response_json["error"]["message"] == expected_message



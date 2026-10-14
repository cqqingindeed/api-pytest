import requests
from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        self.headers = {}
        self.authenticated = authenticated
        if authenticated:
            logger.info("Initializing authenticated API client for %s", email)
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"
        else:
            logger.info("Initializing unauthenticated API client")

    def login(self, email, password):
        logger.debug(f"Attempting login at /api/v1/auto/login as {email}")
        url = f"/api/v1/auth/login"
        payload = {"email": email, "password": password}
        response_body = self.post_json(url, payload)
        access_token = response_body["access_token"]
        logger.info("Login successful for %s", email)
        return access_token


    def get(self, endpoint, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        logger.debug(f"GET {url} expecting {expected_status_code}")
        response = requests.get(url, headers=headers)
        logger.info(f"GET {url} -> {response.status_code}")
        assert response.status_code == expected_status_code, f"expect {expected_status_code}, actual is {response.status_code}"
        self.verify_status_code(response, expected_status_code, url)
        return response


    def get_json(self, endpoint, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        # url = self.build_url(endpoint)
        response = self.get(endpoint, headers, expected_status_code)
        return response.json()


    def post(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        # breakpoint()
        response = requests.post(url, json=data, headers=headers)
        # assert response.status_code == expected_status_code
        self.verify_status_code(response, expected_status_code, url)
        return response


    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        # breakpoint()
        # url = self.build_url(endpoint)
        response = self.post(endpoint, data, headers, expected_status_code)
        return response.json()

    
    def build_headers(self, headers=None):
        if self.authenticated:
            return {**self.headers, **(headers or {})} # combining two dicts
        return headers


    def verify_status_code(self, response, expected_status_code, url):
        assert response.status_code == expected_status_code, f"Expected code: {expected_status_code}; actual code: {response.status_code}; URL:{url}"


    def build_url(self, endpoint):
        return f"{BASE_URL}{endpoint}"


    def delete(self, endpoint, expected_status_code=204):
        headers = self.build_headers()
        url = self.build_url(endpoint)
        logger.debug(f"GET {url} expecting {expected_status_code}")
        # breakpoint()
        response = requests.delete(url, headers=headers)
        logger.info(f"Delete {url} -> {response.status_code}")
        # assert response.status_code == expected_status_code, f"expect 204, actual is {response.status_code}"
        self.verify_status_code(response, expected_status_code, url)
        assert response.headers, "verify response header has something."
        return response


    def patch(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        # breakpoint()
        response = requests.patch(url, json=data, headers=headers)
        # assert response.status_code == expected_status_code
        self.verify_status_code(response, expected_status_code, url)
        return response


    def patch_json(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        # breakpoint()
        # url = self.build_url(endpoint)
        response = self.patch(endpoint, data, headers, expected_status_code)
        return response.json()


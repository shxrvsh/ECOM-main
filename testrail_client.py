import requests

class TestRailClient:
    def __init__(self, base_url, user, api_key, run_id):
        self.base_url = base_url.rstrip("/")
        self.auth = (user, api_key)
        self.headers = {"Content-Type": "application/json"}
        self.run_id = run_id

    def add_result(self, case_id, status_id, comment=""):
        """
        Push result for a TestRail case inside a run.
        status_id: 1=Passed, 2=Blocked, 5=Failed
        """
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{self.run_id}/{case_id}"
        payload = {"status_id": status_id, "comment": comment}
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
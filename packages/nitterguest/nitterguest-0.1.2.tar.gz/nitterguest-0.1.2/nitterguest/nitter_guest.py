import requests
from typing import Optional
from logging import getLogger

class NitterGuest:
    def __init__(self, auth_token: str) -> None:
        self.auth_token = auth_token
        self.logger = getLogger(__name__)

    def get_guest_oauth_token(self) -> dict:
        guest_token = self._get_guest_token()
        flow_token = self._get_flow_token(guest_token=guest_token)
        oauth_token = self._get_oauth_token(guest_token=guest_token, flow_token=flow_token)
        return oauth_token

    def _get_header(self, guest_token: Optional[str] = None, mock_ua: bool = False) -> dict:
        header = {
            "Authorization": "Bearer {}".format(self.auth_token)
        }
        if guest_token:
            header["X-Guest-Token"] = guest_token
        if mock_ua:
            header["Content-Type"] = "application/json"
            header["User-Agent"] = "TwitterAndroid/10.10.0"
        return header

    def _get_guest_token(self) -> str:
        req = requests.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=self._get_header())
        if req.status_code == 200:
            t = req.json()["guest_token"]
            self.logger.info(f"guest token received: {t}")
            return t
        raise ConnectionError()

    def _get_flow_token(self, guest_token: str) -> str:
        req = requests.post(
            "https://api.twitter.com/1.1/onboarding/task.json?flow_name=welcome",
            headers=self._get_header(
                guest_token=guest_token,
                mock_ua=True
                ),
            json={
                "flow_token": None,
                "input_flow_data": {
                    "flow_context": {"start_location": {"location":"splash_screen"}}
                    }
                }
            )
        if req.status_code == 200:
            t = req.json()["flow_token"]
            self.logger.info(f"flow token received: {t}")
            return t
        raise ConnectionError()

    def _get_oauth_token(self, guest_token: str, flow_token: str) -> dict[str, str]:
        req = requests.post(
            "https://api.twitter.com/1.1/onboarding/task.json",
            headers=self._get_header(
                guest_token=guest_token,
                mock_ua=True
                ),
            json={
                "flow_token": flow_token,
                "subtask_inputs": [
                    { "open_link": {"link":"next_link"}, "subtask_id": "NextTaskOpenLink" }
                    ]
                }
            )
        if req.status_code == 200:
            if req.json()["subtasks"][0]:
                oauth_account_info = req.json()["subtasks"][0]["open_account"]
                t = {
                    "oauth_token": oauth_account_info["oauth_token"],
                    "oauth_token_secret": oauth_account_info["oauth_token_secret"]
                    }
                self.logger.info(f"oauth token received: {t}")
                return t
        raise ConnectionError()

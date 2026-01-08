import requests
import time
from config.settings import LOGIN_URL, REFRESH_URL

class AuthService:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.access_token = None
        self.refresh_token = None
        self.expires_at = 0

    def login(self):
        response = requests.post(
            LOGIN_URL,
            json={
                "username": self.username,
                "password": self.password
            },
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data.get("refresh_token")
        self.expires_at = time.time() + data["expires_in"]

    def refresh(self):
        response = requests.post(
            REFRESH_URL,
            json={"refresh_token": self.refresh_token},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.expires_at = time.time() + data["expires_in"]

    def get_headers(self):
        if not self.access_token or time.time() >= self.expires_at:
            if self.refresh_token:
                self.refresh()
            else:
                self.login()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

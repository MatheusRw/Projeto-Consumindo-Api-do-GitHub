import json
import time
import requests
from config import settings


class AuthService:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = 0

        if settings.TOKEN_FILE:
            self._load_static_token()

    def _load_static_token(self):
        try:
            with open(settings.TOKEN_FILE, "r", encoding="utf-8") as f:
                self.access_token = json.load(f)["access_token"]
        except FileNotFoundError:
            pass

    def _has_login(self):
        return all([
            settings.LOGIN_URL,
            settings.USERNAME,
            settings.PASSWORD
        ])

    def _token_expired(self):
        return self.expires_at and time.time() >= self.expires_at

    def login(self):
        response = requests.post(
            settings.LOGIN_URL,
            json={
                "username": settings.USERNAME,
                "password": settings.PASSWORD
            },
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data.get("refresh_token")
        self.expires_at = time.time() + data.get("expires_in", 0)

    def refresh(self):
        if not settings.REFRESH_URL or not self.refresh_token:
            self.login()
            return

        response = requests.post(
            settings.REFRESH_URL,
            json={"refresh_token": self.refresh_token},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.expires_at = time.time() + data.get("expires_in", 0)

    def get_headers(self):
        if self._has_login():
            if not self.access_token:
                self.login()
            elif self._token_expired():
                self.refresh()

        return {
            #"Authorization": f"Bearer {self.access_token}",
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github+json"
            #"Content-Type": "application/json"
        }

import requests
from services.auth import AuthService
from config.settings import REPOS_ENDPOINT, PER_PAGE

class GitHubClient:
    def __init__(self):
        self.auth = AuthService()

    def fetch_all_repos(self):
        page = 1
        repos = []

        while True:
            response = requests.get(
                REPOS_ENDPOINT,
                headers=self.auth.get_headers(),
                params={
                    "per_page": PER_PAGE,
                    "page": page
                },
                timeout=10
            )

            if response.status_code == 401:
                self.auth.refresh_token()
                continue

            response.raise_for_status()
            data = response.json()

            if not data:
                break

            repos.extend(data)
            page += 1

        return repos

import json
from config.settings import TOKEN_FILE

class AuthService:
    def __init__(self):
        self.token = self._load_token()

    def _load_token(self):
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data["access_token"]

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def refresh_token(self):
        """
        GitHub tokens não expiram automaticamente.
        Aqui é um exemplo REAL de onde você renovaria o token
        caso a API fosse OAuth.
        """
        self.token = self._load_token()

from services.client import GitHubClient
from services.extractor import save_to_json


def main():
    client = GitHubClient()
    repos = client.fetch_all_repos()
    save_to_json(repos, "data/repos.json")
    print(f"{len(repos)} repositórios salvos")

if __name__ == "__main__":
    main()

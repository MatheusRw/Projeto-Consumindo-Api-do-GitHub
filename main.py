from services.client import GitHubClient
from services.extractor import save_to_json

OUTPUT_FILE = "data/repos.json"

def main():
    client = GitHubClient()
    repos = client.fetch_all_repos()

    save_to_json(repos, OUTPUT_FILE)

    print(f"{len(repos)} repositórios salvos em {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

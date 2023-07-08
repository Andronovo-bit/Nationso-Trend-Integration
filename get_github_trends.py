import json
import requests
from datetime import datetime
import pathlib

YOUR_GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

class GithubTrend:
    def __init__(self, language='any', date_range='weekly'):
        self.language = language
        self.date_range = date_range
        self.token = YOUR_GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.params = {
            "language": self.language,
            "since": self.date_range
        }

    def fetch_trending_repositories(self):
        # Use requests.Session to reuse the connection and improve performance
        session = requests.Session()
        session.headers.update(self.headers)
        session.params.update(self.params)

        # Use f-strings for formatting and pathlib for handling paths
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_path = pathlib.Path(f"Json/github/github_trends_{current_date}.json")

        # Use a try-except block to handle errors
        try:
            response = session.get("https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc")
            response.raise_for_status()
            data = response.json()

            # Use the json module's dump method to write to the file
            with file_path.open("w") as f:
                json.dump(data, f)

            print(f"Total number of repos: {data['total_count']}")
            for repo in data["items"]:
                print(f"Repo name: {repo['name']}")
                print(f"Repo url: {repo['html_url']}")
                print()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


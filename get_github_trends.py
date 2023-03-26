import json
import requests
from datetime import datetime

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
        current_date = datetime.now().strftime("%Y-%m-%d")
        response = requests.get("https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc", headers=self.headers, params=self.params)
        if response.status_code == 200:
            data = response.json()
            with open(f"Json/github/github_trends_{current_date}.json", "w") as f:
                json.dump(data, f)


            print(f"Total number of repos: {data['total_count']}")
            for repo in data["items"]:
                print(f"Repo name: {repo['name']}")
                print(f"Repo url: {repo['html_url']}")
                print()
        else:
            print(f"Request failed: {response.status_code}")

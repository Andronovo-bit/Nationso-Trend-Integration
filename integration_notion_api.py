import requests
class NotionAPI:
    def __init__(self, token, version="2022-02-22"):
        self.token = token
        self.version = version
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": self.version
        }
        self.notion_api_url = "https://api.notion.com/v1/"

    
    def create_database(self, data):
        response = requests.post(self.notion_api_url + "databases", headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status {response.status_code}: {response.text}")
            return None
    
    def create_page(self,data):
        response = requests.post(self.notion_api_url + "pages", headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status {response.status_code}: {response.text}") 
            return None

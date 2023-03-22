import time
from integration_notion_api import NotionAPI
from get_github_trends import GithubTrend
import json
from datetime import datetime

YOUR_NOTIONAPI_TOKEN =  "YOUR_NOTIONAPI_TOKEN"
YOUR_NOTIONAPI_ACCESS_PAGE_ID = "YOUR_NOTIONAPI_ACCESS_PAGE_ID"

if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Set the Notion API token and database ID
    token = YOUR_NOTIONAPI_TOKEN
    #database_id = "your_database_id_here"

    # Create an instance of the NotionAPI class
    notion_api = NotionAPI(token)

    # Open the JSON file and load the data
    with open("Json/github_weekly_database.json", "r") as f:
        read_json_file = json.load(f)

    # Replace the page_id value with a new ID
    read_json_file["parent"]["page_id"] = YOUR_NOTIONAPI_ACCESS_PAGE_ID
    
    database_response = notion_api.create_database(read_json_file)

    if database_response:
        # Get the ID of the newly created database
        database_id = database_response["id"]

        # Open the JSON file and load the data
        with open("Json/github_weekly_page.json", "r") as f:
            read_json_file = json.load(f)

        read_json_file["parent"]["database_id"] = database_id
        read_json_file["properties"]["Date"]["date"]["start"] = current_date
        read_json_file["properties"]["Name"]["title"][0]["text"]["content"] = f"Trending Repositories on {current_date}"      

        # Create a new page in the database
        page_response = notion_api.create_page(read_json_file)

        if page_response:
            # Get the ID of the newly created page
            page_id = page_response["id"]

            with open("Json/github_weekly_repos_database.json", "r") as f:
                read_json_file = json.load(f)

            # Replace the page_id value with a new ID
            read_json_file["parent"]["page_id"] = page_id
            read_json_file["title"][0]["text"]["content"] = "Githubweekly Repos"

            database_response = notion_api.create_database(read_json_file)

            if database_response:
                print("New row added to database:", database_response["id"])
                
                github_trend = GithubTrend()
                github_trend.fetch_trending_repositories()

                with open(f"Json/github_trends_{current_date}.json", "r") as f:
                    response_data = json.load(f)

                items = response_data['items']
                with open("Json/github_weekly_repos_page.json", "r") as f:
                    read_json_file = json.load(f)

                for item in items:
                    read_json_file["parent"]["database_id"] = database_response["id"]
                    read_json_file["properties"]["Name"]["title"][0]["text"]["content"] = item['full_name']
                    read_json_file["properties"]["Description"]["rich_text"][0]["text"]["content"] = item['description']
                    read_json_file["properties"]["Number_of_Star"]["number"] = item['stargazers_count']
                    read_json_file["properties"]["Language"]["rich_text"][0]["text"]["content"] = item['language'] if item['language'] else " "
                    read_json_file["properties"]["Link"]["url"] = item['html_url']
                    read_json_file["properties"]["Update_Date"]["date"]["start"] = item['updated_at']
                    read_json_file["properties"]["Avatar"]["files"][0]["external"]["url"] = item['owner']['avatar_url']
                    page_response = notion_api.create_page(read_json_file)
                    time.sleep(0.1)


            else:
                print("Failed to add row to database")
        else:
            print("Failed to create page in database")
    else:
        print("Failed to create database")



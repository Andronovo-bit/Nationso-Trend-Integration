import time
import json
from datetime import datetime

from get_github_trends import GithubTrend
from get_dailydev_stream import DailyDevScraper
from get_medium_recommended import MediumScraper
from integration_notion_api import NotionAPI
from json_database import JsonDatabase

YOUR_NOTIONAPI_TOKEN =  ""
YOUR_NOTIONAPI_ACCESS_PAGE_ID = ""
YOUR_DAILY_DEV_COOKIE = ""

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

def get_database_id(search_platform, database_template, notion_api: NotionAPI):
    # Load JSON templates
    db = JsonDatabase('data.json')
    try:
        id = db.find_data(search_platform).pop()["page_id"]
        database_id = id
    except IndexError:
        # Create database
        database_response = notion_api.create_database(database_template)
        if not database_response:
            print("Failed to create database")
            return None
        db.write_data(database_response["id"], search_platform)
        # Get the ID of the newly created database
        database_id = database_response["id"]
        print("New database created for {}: {}".format(search_platform, database_response["id"]))
    return database_id

def create_github_trends(notion_api):
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Load JSON templates
    database_template = load_json("Json/github/github_weekly_database.json")
    page_template = load_json("Json/github/github_weekly_page.json")
    repos_database_template = load_json("Json/github/github_weekly_repos_database.json")
    repos_page_template = load_json("Json/github/github_weekly_repos_page.json")

    # Replace the Notion API access page ID
    database_template["parent"]["page_id"] = YOUR_NOTIONAPI_ACCESS_PAGE_ID
    
    weekly_database_id = get_database_id("github", database_template,notion_api)

    # Replace the database_id value with a new ID for the weekly page
    page_template["parent"]["database_id"] = weekly_database_id
    page_template["properties"]["Date"]["date"]["start"] = current_date
    page_template["properties"]["Name"]["title"][0]["text"]["content"] = f"Trending Repositories on {current_date}"

    # Create weekly page
    weekly_page_response = notion_api.create_page(page_template)
    if not weekly_page_response:
        print("Failed to create weekly page")
        return

    # Get the ID of the newly created weekly page
    weekly_page_id = weekly_page_response["id"]

    # Replace the page_id value with a new ID for the weekly repos database
    repos_database_template["parent"]["page_id"] = weekly_page_id
    repos_database_template["title"][0]["text"]["content"] = "Githubweekly Repos"

    # Create weekly repos database
    repos_database_response = notion_api.create_database(repos_database_template)
    if not repos_database_response:
        print("Failed to create weekly repos database")
        return

    # Fetch trending repositories
    github_trend = GithubTrend()
    github_trend.fetch_trending_repositories()
    
    # Load response data
    response_data = load_json(f"Json/github/github_trends_{current_date}.json")
    items = response_data['items']

    # Create weekly repos page
    for item in items:
        repos_page_template["parent"]["database_id"] = repos_database_response["id"]
        repos_page_template["properties"]["Name"]["title"][0]["text"]["content"] = item['full_name']
        repos_page_template["properties"]["Description"]["rich_text"][0]["text"]["content"] = item['description']
        repos_page_template["properties"]["Number_of_Star"]["number"] = item['stargazers_count']
        repos_page_template["properties"]["Language"]["rich_text"][0]["text"]["content"] = item.get('language') or " "
        repos_page_template["properties"]["Link"]["url"] = item['html_url']
        repos_page_template["properties"]["Update_Date"]["date"]["start"] = item['updated_at']
        repos_page_template["properties"]["Avatar"]["files"][0]["external"]["url"] = item['owner']['avatar_url']
        notion_api.create_page(repos_page_template)
        time.sleep(0.1)

def create_dailydev_stream(notion_api):
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Load JSON templates
    database_json = load_json("Json/dailydev/dailydev_stream_database.json")
    page_json = load_json("Json/dailydev/dailydev_stream_page.json")
    repos_database_json = load_json("Json/dailydev/dailydev_stream_repos_database.json")
    repos_page_json = load_json("Json/dailydev/dailydev_stream_repos_page.json")

    # Replace necessary values in JSON files
    database_json["parent"]["page_id"] = YOUR_NOTIONAPI_ACCESS_PAGE_ID
    database_json["title"][0]["text"]["content"] = "Daily Dev Stream"
    page_json["properties"]["Date"]["date"]["start"] = current_date
    page_json["properties"]["Name"]["title"][0]["text"]["content"] = f"Trending Stream on {current_date}"

    # Get database ID
    database_id = get_database_id("daily_dev", database_json,notion_api)
    
    # Get database ID and create page
    page_json["parent"]["database_id"] = database_id
    page_response = notion_api.create_page(page_json)
    if not page_response:
        print("Failed to create page in database")
        return
    
    # Get page ID and create another database and its pages
    page_id = page_response["id"]
    repos_database_json["parent"]["page_id"] = page_id
    repos_database_json["title"][0]["text"]["content"] = "DailyDev Trend Repos"
    database_response = notion_api.create_database(repos_database_json)
    if not database_response:
        print("Failed to add row to database")
        return
    
    print("New row added to database:", database_response["id"])
    
    # Scrape data and add to database
    file_name = f"Json/dailydev/dailydev_trends_{current_date}.json"
    daily_dev_scraper = DailyDevScraper(YOUR_DAILY_DEV_COOKIE)
    daily_dev_scraper.scrape(filename=file_name)

    with open(file_name, "r") as f:
        response_data = json.load(f)
    
    items = response_data['data']['page']['edges']
    for item in items:
        node = item['node']
        repos_page_json["parent"]["database_id"] = database_response["id"]
        repos_page_json["properties"]["Name"]["title"][0]["text"]["content"] = node.get('title') or ""
        repos_page_json["properties"]["Source"]["rich_text"][0]["text"]["content"] = node['source'].get('name') or ""
        repos_page_json["properties"]["Tags"]["rich_text"][0]["text"]["content"] = ', '.join(node.get('tags', []))
        repos_page_json["properties"]["Type"]["rich_text"][0]["text"]["content"] = node.get('type') or ""
        repos_page_json["properties"]["Link"]["url"] = node.get('permalink') or ""
        repos_page_json["properties"]["Created_Date"]["date"]["start"] = node.get('createdAt','').split('T')[0] or ""
        repos_page_json["properties"]["Image"]["files"][0]["external"]["url"] = node.get('image') or ""
        notion_api.create_page(repos_page_json)
        time.sleep(0.1)

def create_medium_recommend(notion_api):
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Load JSON templates
    database_template = load_json("Json/medium/medium_recommend_database.json")
    page_template = load_json("Json/medium/medium_recommend_page.json")
    repos_database_template = load_json("Json/medium/medium_recommend_repos_database.json")
    repos_page_template = load_json("Json/medium/medium_recommend_repos_page.json")

    # Replace the Notion API access page ID
    database_template["parent"]["page_id"] = YOUR_NOTIONAPI_ACCESS_PAGE_ID

    # Get database ID
    recommend_database_id = get_database_id("medium", database_template, notion_api)

    # Replace the database_id value with a new ID for the weekly page
    page_template["parent"]["database_id"] = recommend_database_id
    page_template["properties"]["Date"]["date"]["start"] = current_date
    page_template["properties"]["Name"]["title"][0]["text"]["content"] = f"Recommend Articles on {current_date}"

    # Create recommend page
    recommend_page_response = notion_api.create_page(page_template)
    if not recommend_page_response:
        print("Failed to create weekly page")
        return

    # Get the ID of the newly created weekly page
    recommend_page_id = recommend_page_response["id"]

    # Replace the page_id value with a new ID for the weekly repos database
    repos_database_template["parent"]["page_id"] = recommend_page_id
    repos_database_template["title"][0]["text"]["content"] = "Medium Recommend Articles"

    # Create recommend repos database
    repos_database_response = notion_api.create_database(repos_database_template)
    if not repos_database_response:
        print("Failed to create weekly repos database")
        return

    # Fetch recommend articles from Medium
    medium_scraper = MediumScraper()
    medium_scraper.scrape()

    # Load response data
    response_data = load_json(f"Json/medium/medium_recommended_{current_date}.json")
    items = response_data
    # Create weekly repos page
    for item in items:
        repos_page_template["parent"]["database_id"] = repos_database_response["id"]
        repos_page_template["properties"]["Name"]["title"][0]["text"]["content"] = item['name']
        repos_page_template["properties"]["Reason"]["rich_text"][0]["text"]["content"] = item.get('reason') or ""
        repos_page_template["properties"]["Creator_Name"]["rich_text"][0]["text"]["content"] = item['username']
        repos_page_template["properties"]["Clap_Count"]["number"] = item['clapCount']
        repos_page_template["properties"]["Reading_Time"]["number"] =round(item['readingTime'], 2) 
        repos_page_template["properties"]["Tags"]["rich_text"][0]["text"]["content"] = ', '.join(item.get('tags', []))
        repos_page_template["properties"]["Link"]["url"] = item['mediumUrl']
        repos_page_template["properties"]["Published_Date"]["date"]["start"] = datetime.fromtimestamp(item['date']/1000.0).strftime('%Y-%m-%d %H:%M:%S') 
        repos_page_template["properties"]["Image"]["files"][0]["external"]["url"] = item['previewImage']
        notion_api.create_page(repos_page_template)
        time.sleep(0.1)

if __name__ == "__main__":
    # Set the Notion API token and database ID
    token = YOUR_NOTIONAPI_TOKEN

    # Create an instance of the NotionAPI class
    notion_api = NotionAPI(token)

    # Create github trends
    create_github_trends(notion_api)

    # Create dailydev stream
    create_dailydev_stream(notion_api)

    # Create medium recommend
    create_medium_recommend(notion_api)

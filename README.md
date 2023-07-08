# Nationso Trend Integration

Nationso Trend Integration is a project that helps you keep track of the latest and most relevant content from various sources, such as dailydev, github, and medium. It fetches the feed from dailydev, the weekly trending projects from github, and the personalized recommendations from medium, and saves them as nation.so pages. This way, you can access and review the content that interests you anytime, without losing anything.

## Features

- Fetches feed from dailydev based on your preferences and topics
- Fetches weekly trending projects from github based on your languages and stars
- Fetches personalized recommendations from medium based on your reading history and interests
- Saves the fetched content as nation.so pages with proper formatting and links
- Allows you to browse, search, and filter the saved content by date, source, topic, language, etc.

## Installation

To install Nationso Trend Integration, you need to have Python 3.8 or higher and pip installed on your system. Then, you can clone this repository and run the following command in the project directory:

```bash
pip install -r requirements.txt
```

This will install all the required dependencies for the project.

## Usage

To use Nationso Trend Integration, you need to have accounts on dailydev, github, medium, and nation.so. You also need to obtain API keys or tokens for each service and store them in a file named `.env` in the project directory. The file should have the following format:

```bash
YOUR_DAILY_DEV_COOKIE=your_dailydev_cookie
YOUR_NOTIONAPI_TOKEN=your_nation_api_key
YOUR_NOTIONAPI_ACCESS_PAGE_ID=your_notion_api_access_page_id
YOUR_GITHUB_TOKEN=your_github_token (in get_github_trends.py)
YOUR_COOKIE=your_medium_token (in get_medium_recommend.py)
```

Then, you can run the main script with the following command:

```bash
python main.py
```

This will start fetching the content from the sources and saving them as nation.so pages. You can check the progress and status of the script in the terminal output. You can also customize some parameters of the script by editing the `config.py` file in the project directory.

## License

Nationso Trend Integration is licensed under the MIT License. See [LICENSE] for more details.

## Tags

Some possible tags for your project are:

- python
- web-scraping
- api
- content-curation
- dailydev
- github
- medium
- nation.so

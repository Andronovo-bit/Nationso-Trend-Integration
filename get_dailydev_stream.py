import json
import requests
import pathlib

class DailyDevScraper:
    
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            "authority": "app.daily.dev",
            "accept": "*/*",
            "accept-language": "tr,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": self.cookie,
            "origin": "https://app.daily.dev",
            "referer": "https://app.daily.dev/",
            "sec-ch-ua": '^"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111""',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        
        self.graphql_data = {
            "query": """
              query Feed(
                $loggedIn: Boolean! = false
                $first: Int
                $after: String
                $ranking: Ranking
                $version: Int
                $supportedTypes: [String!] = ["article", "share"]
              ) {
                page: feed(
                  first: $first
                  after: $after
                  ranking: $ranking
                  version: $version
                  supportedTypes: $supportedTypes
                ) {
                  ...FeedPostConnection
                }
              }

              fragment FeedPostConnection on PostConnection {
                pageInfo {
                  hasNextPage
                  endCursor
                }
                edges {
                  node {
                    ...FeedPost
                    ...UserPost @include(if: $loggedIn)
                  }
                }
              }

              fragment FeedPost on Post {
                id
                title
                createdAt
                image
                readTime
                source {
                  ...SourceShortInfo
                }
                sharedPost {
                  ...SharedPostInfo
                }
                permalink
                numComments
                numUpvotes
                commentsPermalink
                scout {
                  ...UserShortInfo
                }
                author {
                  ...UserShortInfo
                }
                trending
                tags
                type
                private
              }

              fragment SharedPostInfo on Post {
                id
                title
                image
                readTime
                permalink
                commentsPermalink
                summary
                createdAt
                private
                scout {
                  ...UserShortInfo
                }
                author {
                  ...UserShortInfo
                }
                type
                tags
                source {
                  ...SourceShortInfo
                }
              }

              fragment SourceShortInfo on Source {
                id
                handle
                name
                permalink
                description
                image
                type
                active
              }

              fragment UserShortInfo on User {
                id
                name
                image
                permalink
                username
                bio
              }

              fragment UserPost on Post {
                read
                upvoted
                commented
                bookmarked
              }
            """,
            "variables": {
                "version": 10,
                "ranking": "POPULARITY",
                "first": 17,
                "loggedIn": True
            }
        }

    def scrape(self, filename='daily.json'):
        # Use requests.Session to reuse the connection and improve performance
        session = requests.Session()
        session.headers.update(self.headers)

        # Use pathlib to handle paths
        file_path = pathlib.Path(filename)

        # Use a try-except block to handle errors
        try:
            response = session.post("https://app.daily.dev/api/graphql", json=self.graphql_data)
            response.raise_for_status()
            data = response.json()

            # Use the json module's dump method to write to the file
            with file_path.open("w") as f:
                json.dump(data, f)
        except requests.exceptions.RequestException as e:
            # Print the error message if the request was unsuccessful
            print(f"Request failed: {e}")


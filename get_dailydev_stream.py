import json
import requests

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
        response = requests.post("https://app.daily.dev/api/graphql", headers=self.headers, json=self.graphql_data)
        if response.status_code == 200:
            data = response.json()
            with open(filename, "w") as f:
                json.dump(data, f)
        else:
            print(f"Request failed: {response.status_code}")

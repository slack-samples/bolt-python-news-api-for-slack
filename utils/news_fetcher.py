from typing import List, Optional

import requests
import logging

from utils.articles import Article

default_logger = logging.getLogger(__name__)


class NewsFetcher:
    def __init__(self, news_api_key: str, logger: Optional[logging.Logger] = None):
        self.api_key = news_api_key
        self.logger = logger or default_logger

    def fetch_articles(self, query: str, num_articles: int = 3) -> List[Article]:
        params = {
            "apiKey": self.api_key,
            "q": query,
            "language": "en",
            "pageSize": num_articles,
            "sortBy": "publishedAt",
        }
        url = "https://newsapi.org/v2/everything" if query else "https://newsapi.org/v2/top-headlines"

        if query:
            # For more complex queries, see the Advanced Search options here:
            # https://newsapi.org/docs/endpoints/everything
            params["q"] = query.replace(",", " OR ").replace("、", " OR ")
        else:
            del params["q"]
        try:
            self.logger.info(
                f"Fetching articles from NewsAPI {url} query: {params['q']} number of articles: {params['pageSize']}"
            )
            response = requests.get(url=url, params=params)
        except Exception as err:
            self.logger.error(err)
        response_body = response.json()

        return [Article(**article) for article in response_body.get("articles")]

    def format_article(self, article: Article) -> List[dict]:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": article.title},
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"⏱ {article.publishedAt.strftime('%Y-%m-%d %H:%M:%S')}",
                    }
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{article.description[:200]}... <{article.url}|Continue reading...>",
                },
                "accessory": {
                    "type": "image",
                    "image_url": article.urlToImage,
                    "alt_text": "News article image",
                },
            },
        ]

        # Remove the image block if there are no images from the News API
        if not article.urlToImage:
            del blocks[2]["accessory"]
            return blocks
        return blocks

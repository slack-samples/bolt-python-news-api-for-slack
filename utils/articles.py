from dataclasses import dataclass
from datetime import datetime

import pytz


@dataclass
class Source:
    id: str
    name: str


@dataclass
class Article:
    source: Source
    author: str
    title: str
    description: str
    url: str
    urlToImage: str
    publishedAt: datetime
    content: str

    def __post_init__(self):
        self.publishedAt = datetime.fromisoformat(self.publishedAt[:-1]).replace(tzinfo=pytz.timezone("UTC"))

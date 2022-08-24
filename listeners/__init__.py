from slack_bolt import App

from listeners import steps
from utils.news_fetcher import NewsFetcher


def register_listeners(app: App, news_fetcher: NewsFetcher):
    steps.register(app, news_fetcher)

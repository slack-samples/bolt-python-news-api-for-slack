from slack_bolt import App

from listeners.steps import workflow_step
from utils.news_fetcher import NewsFetcher


def register(app: App, news_fetcher: NewsFetcher):
    workflow_step.enable_workflow_step(app, news_fetcher)

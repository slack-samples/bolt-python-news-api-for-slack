import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners
from utils.news_fetcher import NewsFetcher

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
news_api_key = os.environ["NEWS_API_KEY"]
logging.basicConfig(level=logging.DEBUG)

# Register Listeners
register_listeners(app, NewsFetcher(news_api_key))

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()

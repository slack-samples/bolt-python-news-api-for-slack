import logging
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from workflow_step import enable_workflow_step

logging.basicConfig(level=logging.DEBUG)

newsapi_api_key = os.environ["NEWS_API_KEY"]

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

enable_workflow_step(app, newsapi_api_key)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

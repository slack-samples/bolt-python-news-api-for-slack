from slack_bolt import App

from listeners.steps import workflow_step


def register(app: App, news_fetcher):
    # Your app will answer with the following callback functions when presented with workflow events
    workflow_step.enable_workflow_step(app, news_fetcher)

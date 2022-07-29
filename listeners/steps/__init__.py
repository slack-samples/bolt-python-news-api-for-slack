from slack_bolt import App

from .workflow_step import edit, save, execute


def register(app: App):
    # Your app will answer with the following callback functions when presented with workflow events
    app.step("news_step", edit, save, execute)

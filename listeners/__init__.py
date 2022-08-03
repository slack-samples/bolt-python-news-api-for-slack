from listeners import steps


def register_listeners(app, news_fetcher):
    steps.register(app, news_fetcher)

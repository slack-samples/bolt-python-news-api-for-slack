import logging
from typing import Optional, Union

from slack_bolt import Ack, App
from slack_bolt.workflows.step import Configure, Update, Complete, Fail, WorkflowStep
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError

# Keys
from utils.news_fetcher import NewsFetcher

input_channel_ids = "channel_ids"
input_query = "query"
input_num_articles = "num_articles"


def edit(ack: Ack, step: dict, configure: Configure, logger: logging.Logger):
    logger.info("Editing workflow step")
    ack()
    inputs = step.get("inputs")
    blocks = []

    num_article_options = [
        {"text": {"type": "plain_text", "text": "1"}, "value": "1"},
        {"text": {"type": "plain_text", "text": "3"}, "value": "3"},
        {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
    ]

    # Block that determines how many articles to be posted
    num_article_block = {
        "type": "input",
        "block_id": input_num_articles,
        "element": {
            "type": "radio_buttons",
            "options": num_article_options,
            "action_id": "_",
        },
        "label": {"type": "plain_text", "text": "Max number of articles"},
    }

    # Block for specifying which channels to notify
    channels_block = {
        "type": "input",
        "block_id": input_channel_ids,
        "label": {"type": "plain_text", "text": "Channel to post"},
        "element": {
            "type": "multi_channels_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Multiple channels can be chosen.",
            },
            "action_id": "_",
        },
    }

    # Block for users to enter a search query
    query_block = {
        "type": "input",
        "block_id": input_query,
        "optional": True,
        "element": {
            "type": "plain_text_input",
            "action_id": "_",
            "placeholder": {
                "type": "plain_text",
                "text": "technology, sports, finance (Separate multiple terms by a comma)",
            },
        },
        "label": {
            "type": "plain_text",
            "text": "Query (Leave blank for all news articles",
        },
    }

    # Re-populates your configuration blocks with the previously filled out values when editing your workflow step
    if input_num_articles in inputs:
        value = inputs.get(input_num_articles).get("value")
        option = next(
            (o for o in num_article_options if o.get("value") == value),
            None,
        )
        if value is not None:
            num_article_block["element"]["initial_option"] = option

    if input_query in inputs:
        value = inputs.get(input_query).get("value")
        if value is not None:
            query_block["element"]["initial_value"] = value

    if input_channel_ids in inputs:
        value = inputs.get(input_channel_ids).get("value")
        if value is not None:
            channels_block["element"]["initial_channels"] = value.split(",")

    # Add your blocks in the order that you would like them to show up in the modal
    blocks.append(num_article_block)
    blocks.append(channels_block)
    blocks.append(query_block)

    # Pass your blocks to the `configure` function and it will handle the rest
    configure(blocks=blocks)


def save(ack: Ack, view: dict, update: Update, logger: logging.Logger):
    logger.info("Saving workflow step")
    state_values = view["state"]["values"]
    # Extracts the values found within the `state` parameter
    channels = _extract(state_values, input_channel_ids, "selected_channels")
    query = _extract(state_values, input_query, "value")
    num_articles = _extract(state_values, input_num_articles, "selected_option")

    update(
        inputs={
            # Defines what is required from the user for this Workflow step
            input_num_articles: {"value": num_articles},
            input_channel_ids: {"value": ",".join(channels)},
            input_query: {"value": query},
        },
        # Defines what will be produced when this step is properly completed
        outputs=[
            {
                "name": channel_id,
                "type": "text",
                "label": "Posted message timestamp",
            }
            for channel_id in channels
        ],
    )
    ack()


def enable_workflow_step(app: App, news_fetcher: NewsFetcher):
    def execute(step: dict, client: WebClient, complete: Complete, fail: Fail, logger: logging.Logger):
        logger.info("Executing workflow step")
        inputs = step.get("inputs", {})
        try:
            query = inputs.get(input_query).get("value")
            num_articles = int(inputs.get(input_num_articles).get("value"))
            channels = inputs.get(input_channel_ids).get("value").split(",")

            # Calls third-party News API and retrieves articles using inputs from above
            articles = news_fetcher.fetch_articles(query, num_articles)
        except Exception as err:
            fail(error={"message": f"Failed to fetch news articles ({err})"})
            return

        outputs = {}
        try:
            if articles:
                for article in articles:
                    blocks = news_fetcher.format_article(article)
                    for channel in channels:
                        # Send a message to all the specified channels
                        response = client.chat_postMessage(
                            channel=channel,
                            blocks=blocks,
                            unfurl_links=False,
                            unfurl_media=False,
                            text=article.title,
                        )
                        outputs[channel] = response.get("message").get("ts")
            else:
                # Notify the user that no articles were found.
                for channel in channels:
                    response = client.chat_postMessage(
                        channel=channel,
                        text=f"No articles matched your query: {query}.",
                    )
                    outputs[channel] = response.get("message").get("ts")

        except SlackClientError as err:
            fail(error={"message": f"Notification failed ({err})"})

        complete(outputs=outputs)

    app.step(
        WorkflowStep(
            callback_id="news_step",
            edit=edit,
            save=save,
            execute=execute,
        )
    )


def _extract(state_values: dict, key: str, attribute: str) -> Optional[Union[str, list]]:
    v = state_values[key].get("_", {})
    if v is not None and v.get(attribute) is not None:
        attribute_value = v.get(attribute)
        if isinstance(attribute_value, (list, str)):
            return attribute_value
        return attribute_value.get("value")
    return None

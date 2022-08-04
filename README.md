# Bolt for Python News API App

This is a sample Slack app that sends news articles into Slack.

![news-full-gif](https://user-images.githubusercontent.com/1818355/182757792-53223931-7f8d-4543-a15e-5b7699283d18.gif)

For the full details on how this project works, check out the [tutorial](https://api.slack.com/tutorials/news-in-slack) on the Slack API site. Otherwise, continue reading.

日本の方はこちらの記事をご覧ください：https://qiita.com/hello_jun/items/418cca89c52eea13a3fa

## Installation

#### Creating and setting up your Slack App

1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*
4. Review the configuration and click *Create*
6. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.

#### Environment Variables
Before you can run the app, you'll need to store some environment variables.

1. Open your apps configuration page from this list, click **OAuth & Permissions** in the left hand menu, then copy the Bot User OAuth Token. You will store this in your environment as `SLACK_BOT_TOKEN`.
2. Click ***Basic Information** from the left hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Copy this token. You will store this in your environment as `SLACK_APP_TOKEN`.
3. Retrieve your News API key, which can be done for free if you are creating an app for development purposes. On the [sign up page](https://newsapi.org/register), fill in your name, e-mail address, and password, then choose "I am an individual" and submit the form. You will be granted an API key. Store this as the `NEWS_API_KEY` environment variable.

```zsh
# Replace the sections in brackets with your tokens and keys
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
export NEWS_API_KEY=<your-api-key>
```

### Setup Your Local Project
```zsh
# Clone this project onto your machine
git clone https://github.com/slack-samples/bolt-python-news-api-for-slack.git

# Change into this project directory
cd bolt-python-news-api-for-slack

# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Start your local server
python3 app.py
```


## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack apps. With a manifest, you can create an app with a pre-defined configuration, or adjust the configuration of an existing app.

### `app.js`

`app.js` is the entry point for the application and is the file you'll run to start the server. This project aims to keep this file as thin as possible, primarily using it as a way to route inbound requests.

### `/listeners/steps`

Every incoming request is routed to a "listener". Inside this directory, you'll find the `workflow_step.py` file, which defines all the callback functions required to implement a [Steps from Apps](https://api.slack.com/workflows/steps) step. 

### `/utils`

Contains class definitions that make the rest of the project code cleaner.
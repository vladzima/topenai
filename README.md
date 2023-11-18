# topenai
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/vladzima/topenai/master) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/vladzima/topenai/release.yml)

topenai (terminal openai) — a simple command line interface tool to interact with OpenAI.

#### Installation

`pip install topenai`

[How to get an OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)


[OpenAPI models](https://platform.openai.com/docs/models)

To install the latest testing version (may contain more bugs), run:

    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ topenai

#### Features

- Multiple chat threads
- Chat history
- Rename, delete and switch sessions


#### Usage:
Run `topenai` in your terminal

- Enter `/new` to start a new chat (`/n`)
- `/switch <chat_id>` to change chat (`/s`)
- `/list` to list all chats (`/l`)
- `/rename <old_id> <new_id>` to rename a chat (`/r`)
- `/delete <chat_id>` to delete a chat (`/d`)
- `/apikey` to change API key
- `/model` to change model
- `/help` to display this help message (`/h`)
- `/exit` to exit (`/e`)

#### Known issues
- UUIDs of sessions instead of readable names
- Rename is not working

Developing Setup
----------------

If you want to set this package up for directly editing it's source code (for contributing):

1. ***Clone the package***

        git clone https://github.com/vladzima/topenai

2. ***Create a dynamic link***
    This will make the package dynamically update with your local changes:

        pip install -e .

#### TODO
- Make chat history more accesible
- Allow OpenAI API fune-tuning parameters
- Migrate to official OpenAI python API client
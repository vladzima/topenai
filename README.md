# topenai
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/vladzima/topenai/master) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/vladzima/topenai/release.yml)

topenai (terminal openai) — a simple command line interface tool to interact with OpenAI.

#### Installation

`pip install topenai`

[How to get an OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)


[OpenAPI models](https://platform.openai.com/docs/models)

#### Features

- Multiple chat threds
- Chat history
- Rename, delete and switch sessions


#### Commands:
- Enter '/new' to start a new chat ('/n')
- '/switch <chat_id>' to change chat ('/s')
- '/list' to list all chats ('/l')
- '/rename <old_id> <new_id>' to rename a chat ('/r')
- '/delete <chat_id>' to delete a chat ('/d')
- '/apikey' to change API key
- '/model' to change model
- '/help' to display this help message ('/h')
- '/exit' to exit ('/e')

#### Known issues
- UUIDs of sessions instead of readable names
- Rename is not working

#### TODO
- Make chat history more accesible
- Allow OpenAI API fune-tuning parameters
- Migrate to official OpenAI python API client
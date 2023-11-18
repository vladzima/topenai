#!/usr/bin/env python3

from typing import Dict, List, Optional
import json
import os
import requests
import threading
import time
import sys

CONFIG_FILE = 'openai_config.json'
CHAT_HISTORY_FILE = 'chat_histories.json'

# ANSI color and style codes
class Style:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class OpenAIChatbot:
    def __init__(
        self,
        api_key: str,
        model: str = 'gpt-3.5-turbo',
        chat_sessions: Optional[Dict[str, List[Dict[str, str]]]] = None,
        last_chat_id: Optional[str] = None
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.chat_sessions = chat_sessions if chat_sessions is not None else {}
        self.current_chat_id = last_chat_id

    def start_new_session(self) -> None:
        if self.chat_sessions:
            last_id = sorted(self.chat_sessions.keys())[-1]
            try:
                new_id = str(int(last_id) + 1) if last_id.isdigit() else last_id + "_new"
            except ValueError:
                new_id = last_id + "_new"
        else:
            new_id = "1"

        self.chat_sessions[new_id] = []
        self.current_chat_id = new_id
        print("\nNew chat session started with ID:", new_id, "\n")

        self.display_last_messages(self.current_chat_id)

    def switch_session(self, chat_id: str) -> None:
        if chat_id in self.chat_sessions:
            self.current_chat_id = chat_id
            print("\nSwitched to chat ID:", chat_id, "\n")
        else:
            print("\nChat ID not found.\n")

        self.display_last_messages(chat_id)

    def display_last_messages(self, chat_id):
        messages = self.chat_sessions.get(chat_id, [])
        last_two = messages[-2:]  # Get last two messages

        if last_two != []:
            print("\n...\n")
            for msg in last_two:
                speaker = "You" if msg['role'] == 'user' else "GPT"
                history_color = Style.RED if msg['role'] == 'user' else Style.GREEN
                print(f"{Style.BOLD + history_color}{speaker}:{Style.RESET} {msg['content']}")
            print("\n(For a full chat history, please view the chat_histories.json file.)\n")


    def send_message(self, message):
        if self.current_chat_id == 0 or self.current_chat_id not in self.chat_sessions:
            print("\nNo active chat session. Start a new session with '/new'.\n")
            return
        
        # Start blinking indicator in a separate thread
        stop_event = threading.Event()
        indicator_thread = threading.Thread(target=blinking_indicator, args=(stop_event,))
        indicator_thread.start()

        self.chat_sessions[self.current_chat_id].append({"role": "user", "content": message})
        data = {
            "model": self.model,
            "messages": self.chat_sessions[self.current_chat_id]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        
        # Stop the blinking indicator
        stop_event.set()
        indicator_thread.join()

        # Clear the line with the blinking dots
        sys.stdout.write('\r   \r')
        sys.stdout.flush()
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            print(Style.GREEN + Style.BOLD + "GPT:" + Style.RESET, reply, "\n")
            self.chat_sessions[self.current_chat_id].append({"role": "assistant", "content": reply})
        else:
            print("\nError from OpenAI:", response.text, "\n")

    def list_chats(self) -> None:
        if self.chat_sessions:
            print(Style.BOLD + "\nAvailable chat sessions:" + Style.RESET)
            for chat_id in self.chat_sessions:
                print(" -", chat_id)
            print()
        else:
            print(Style.BOLD + "\nNo chat sessions available.\n" + Style.RESET)

    def rename_chat(self, old_id: str, new_id: str) -> None:
        if old_id in self.chat_sessions:
            if new_id in self.chat_sessions:
                print("\nChat ID already exists.\n")
                return

            self.chat_sessions[new_id] = self.chat_sessions.pop(old_id)
            if self.current_chat_id == old_id:
                self.current_chat_id = new_id
            print(f"\nChat session {old_id} renamed to {new_id}.\n")
        else:
            print("\nChat ID not found.\n")

    def delete_chat(self, chat_id: str) -> None:
        if chat_id in self.chat_sessions:
            del self.chat_sessions[chat_id]
            print(f"\nChat session {chat_id} deleted.\n")
            if self.current_chat_id == chat_id:
                self.current_chat_id = None
                if self.chat_sessions:
                    self.current_chat_id = max(self.chat_sessions.keys(), default=None)
                    print("Switched to the last available session:", self.current_chat_id, "\n")
                else:
                    print("No more chat sessions available. Please start a new one.\n")
        else:
            print("\nChat ID not found.\n")
            print("No more chat sessions available. Please start a new one.\n")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as file:
            try:
                chat_data = json.load(file)
                chats = chat_data.get('chats', {})
                last_chat_id = chat_data.get('last_chat_id')
                return chats, last_chat_id
            except json.JSONDecodeError:
                return {}, None
    return {}, None

def save_chat_history(chat_sessions, last_chat_id):
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump({'chats': chat_sessions, 'last_chat_id': last_chat_id}, file, indent=4)

def blinking_indicator(stop_event):
    sys.stdout.write('\n')  # Add an empty line
    sys.stdout.flush()
    while not stop_event.is_set():
        for _ in range(3):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r   \r')
        sys.stdout.flush()
        time.sleep(0.5)

def print_commands():
    commands_list = """
    Commands:
    - Enter '/new' to start a new chat ('/n')
    - '/switch <chat_id>' to change chat ('/s')
    - '/list' to list all chats ('/l')
    - '/rename <old_id> <new_id>' to rename a chat ('/r')
    - '/delete <chat_id>' to delete a chat ('/d')
    - '/apikey' to change API key
    - '/model' to change model
    - '/help' to display this help message ('/h')
    - '/exit' to exit ('/e')
    """
    print(commands_list)

def main():
    config = load_config()
    api_key = config.get('api_key')
    model = config.get('model', 'gpt-3.5-turbo')
    chat_sessions, last_chat_id = load_chat_history()

    if not api_key:
        api_key = input("Enter your OpenAI API Key: ")
        save_config({'api_key': api_key, 'model': model})

    bot = OpenAIChatbot(api_key, model, chat_sessions, last_chat_id)

    print(Style.YELLOW + """\

   __                               _ 
  / /_____  ____  ___  ____  ____ _(_)
 / __/ __ \/ __ \/ _ \/ __ \/ __ `/ / 
/ /_/ /_/ / /_/ /  __/ / / / /_/ / /  
\__/\____/ .___/\___/_/ /_/\__,_/_/   
        /_/                           

Vlad Arbatov — https://github.com/vladzima/topenai        
""" + Style.RESET)
    
    print_commands()

    if not bot.chat_sessions:
        bot.start_new_session()  # Start the first session automatically
    else:
        if bot.current_chat_id:
            print("Entered last used chat session:", bot.current_chat_id, "\n")
            bot.display_last_messages(bot.current_chat_id)

    while True:
        command = input(Style.RED + Style.BOLD + "You:" + Style.RESET + " ")

        if command.startswith('/'):
            if command in ('/new', '/n'):
                bot.start_new_session()
            elif command in ('/switch ','/s '):
                _, chat_id_str = command.split(maxsplit=1)
                try:
                    chat_id = chat_id_str
                    bot.switch_session(chat_id)
                except ValueError:
                    print("\nInvalid chat ID.\n")
            elif command in ('/list','/l'):
                bot.list_chats()
            elif command in ('/rename ','/r '):
                _, old_id, new_id = command.split(maxsplit=2)
                bot.rename_chat(old_id, new_id)
                save_chat_history(bot.chat_sessions, bot.current_chat_id)  # Save changes immediately
            elif command in ('/delete ', '/d '):
                _, chat_id = command.split(maxsplit=1)
                bot.delete_chat(chat_id)
            elif command == '/apikey':
                api_key = input("Enter new API Key: ")
                bot.api_key = api_key
                save_config({'api_key': api_key, 'model': bot.model})
                print("\nAPI Key updated.\n")
            elif command == '/model':
                model = input("Enter model (e.g., gpt-3.5-turbo): ")
                bot.model = model
                save_config({'api_key': bot.api_key, 'model': model})
                print("\nModel updated.\n")
            elif command in ('/help','/h'):
                print_commands()
            if command in ('/exit','/e'):
                save_chat_history(bot.chat_sessions, bot.current_chat_id)
                break
        else:
            bot.send_message(command)

if __name__ == "__main__":
    main()

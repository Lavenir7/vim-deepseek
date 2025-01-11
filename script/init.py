from argparse import ArgumentParser
from yaml import dump, safe_load
from datetime import datetime
import os

# CONSTANTS
SCIPT_PATH = os.path.dirname(__file__)
CHATS_PATH = SCIPT_PATH+"/../assets/chats/"
CHAT_LIST_PATH = CHATS_PATH+".list.yml"
PROMPT_DEFAULT_PATH = SCIPT_PATH+"/../assets/prompts/assistant"
# params
parser = ArgumentParser(description = "init session")
parser.add_argument("session", type=str, default="", help="会话编号")
args = parser.parse_args()

with open(PROMPT_DEFAULT_PATH, 'r', encoding = "utf-8") as rf:
    system_prompt = rf.read()

fmt = lambda role, content: {"role": role, "content": content}
messages = [fmt("system", system_prompt)]

def initChat():
    chat_name = f"chat_{args.session}"
    chat_mark = "Created time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            chat_list = safe_load(rf.read())
        if not chat_list:
            chat_list = dict()
    else:
        chat_list = dict()
    if chat_name not in chat_list:
        chat_list[chat_name] = chat_mark
        with open(CHAT_LIST_PATH, 'w', encoding = "utf-8") as wf:
            wf.write(dump(chat_list))
        with open(CHATS_PATH+chat_name+".yaml", 'w', encoding = "utf-8") as wf:
            wf.write(dump(messages, sort_keys = False))
    return 1

if __name__ == "__main__":
    initChat()

#!/usr/bin/python
from argparse import ArgumentParser
import os

# CONSTANTS
SCRIPT_PATH = os.path.dirname(__file__)
CHATS_PATH = SCRIPT_PATH+"/../assets/chats/"
CHAT_LIST_PATH = CHATS_PATH+".list.yml"
# params
parser = ArgumentParser(description = "DeepSeek-V3 chat")
parser.add_argument("-m", "--model", type = str, default = "1", help = "模式")
parser.add_argument("-i", "--currentId", type = str, default = "-1", help = "当前会话ID")
args = parser.parse_args()
list_model = args.model
current_id = args.currentId

def listSessionId():
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        session_id_list = []
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            for chati in rf:
                session_id = chati.split('_')[1].split(':')[0]
                session_id_list.append(session_id)
        print(' '.join(session_id_list), end = '')

def listChats():
    print("可用会话:")
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            for chati in rf:
                tag = '-'
                session_id = chati.split('_')[1].split(':')[0]
                if session_id == current_id:
                    tag = '>'
                print(f"  {tag} {chati}", end = '')

if __name__ == "__main__":
    if list_model == '0':
        listSessionId()
    elif list_model == '1':
        listChats()
    else:
        print(f"no model: {list_model}")


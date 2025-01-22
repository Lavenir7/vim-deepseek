#!/usr/bin/python
from openai import OpenAI
from argparse import ArgumentParser
from yaml import dump, safe_load
from datetime import datetime
import json
import os

# CONSTANTS
SCIPT_PATH = os.path.dirname(__file__)
CHATS_PATH = SCIPT_PATH+"/../assets/chats/"
CHAT_LIST_PATH = CHATS_PATH+".list.yml"
PROMPT_PATH = SCIPT_PATH+"/../assets/prompts/"
with open(SCIPT_PATH+"/config.json", 'r', encoding = "utf-8") as rf:
    deepseek = json.load(rf)
# params
parser = ArgumentParser(description = f"{deepseek['model']['name']} chat")
parser.add_argument("inputs", type=str, default="", help="输入")
parser.add_argument("-k", "--apikey", type = str, default = "", help = "apikey")
parser.add_argument("-p", "--prompt", type = str, default = "assistant", help = "系统提示内容文件名")
parser.add_argument("-s", "--session", type = str, default = "0", help = "会话编号")
args = parser.parse_args()

def myWarning(info: str):
    print(f"\033[93mWarning: {info}\033[0m")

apiKey = args.apikey
for prompt_path_i in (args.prompt, PROMPT_PATH+args.prompt):
    if os.path.exists(prompt_path_i) and os.path.isfile(prompt_path_i):
        with open(prompt_path_i, 'r', encoding = "utf-8") as rf:
            system_prompt = rf.read()
        break
else:
    myWarning(f"系统提示内容不存在 : {args.prompt}")
    system_prompt = ""
session_id = args.session

def loadChat(chat_name: str):
    global messages
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            chat_list = safe_load(rf.read())
            if not chat_list:
                chat_list = dict()
    else:
        chat_list = dict()
    # if chat_name not in chat_list.keys():
    #     myWarning(f"会话 {chat_name} 不存在")
    #     return 0
    if chat_name not in chat_list.keys():
        saveChat(chat_name)
    with open(CHATS_PATH+chat_name+".yaml", 'r', encoding = "utf-8") as rf:
        messages = safe_load(rf.read())
    # print(f"已加载会话: {chat_name}")
    return 1

def saveChat(chat_name: str, chat_mark: str = ''):
    if chat_mark == '':
        chat_mark = "Created time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            chat_list = safe_load(rf.read())
        if not chat_list:
            chat_list = dict()
    else:
        chat_list = dict()
    # if chat_name in chat_list.keys():
    #     myWarning(f"会话 {chat_name} 已存在, 是否覆盖？ (yes/no) ")
    #     confirm = input()
    #     if confirm.lower() not in ('y', "yes"):
    #         return 0
    chat_list[chat_name] = chat_mark
    with open(CHAT_LIST_PATH, 'w', encoding = "utf-8") as wf:
        wf.write(dump(chat_list))
    with open(CHATS_PATH+chat_name+".yaml", 'w', encoding = "utf-8") as wf:
        wf.write(dump(messages, sort_keys = False))
    # print(f"已保存会话: {chat_name}")
    return 1

def showTokens(usage):
    print("\n\n"+"-"*3+"\n")
    print(f"- total tokens : {usage.total_tokens} ({usage.completion_tokens} + {usage.prompt_tokens})")
    print(f"- prompt tokens (hit+miss) : {usage.prompt_tokens} ({usage.prompt_cache_hit_tokens} + {usage.prompt_cache_miss_tokens})")
    if usage.completion_tokens_details:
        print(f"completion tokens details: {usage.completion_tokens_details}")
    if usage.prompt_tokens_details:
        print(f"prompt tokens details: {usage.prompt_tokens_details}")
    print("\n"+"-"*3+"\n")


fmt = lambda role, content: {"role": role, "content": content}

client = OpenAI(api_key = apiKey, base_url = deepseek["api_url"])
messages = [fmt("system", system_prompt)]

if __name__ == "__main__":
    msg = args.inputs
    loadChat(f"chat_{session_id}")
    messages.append(fmt("user", msg))
    response = client.chat.completions.create(
        model = deepseek["model"]["api_use"],
        messages = messages,
        stream = True
    )
    response_reason_contents = ""
    response_contents = ""
    isreason = True if deepseek["model"]["name"] == "DeepSeek-R1" else False
    for res in response:
        if isreason:
            res_reason_content = res.choices[0].message.reasoning_content
        else:
            res_content = res.choices[0].message.content
        # change here
        if res_reason_content:
            response_reason_contents += res_reason_content
        if res_content:
            response_contents += res_content
        print(res_content, end = '', flush = True)
    messages.append(fmt("assistant", response_contents))
    showTokens(res.usage)
    saveChat(f"chat_{session_id}")


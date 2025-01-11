#!/usr/bin/python
from openai import OpenAI
from argparse import ArgumentParser
import os

# CONSTANTS
SCIPT_PATH = os.path.dirname(__file__)
PROMPT_PATH = SCIPT_PATH+"/../assets/prompts/"

def myWarning(info: str):
    print(f"\033[93mWarning: {info}\033[0m")

parser = ArgumentParser(description="DeepSeekV3")

parser.add_argument("inputs", type=str, default="", help="输入")
parser.add_argument("-k", "--apikey", type = str, default = "", help = "apikey")
parser.add_argument("-p", "--prompt", type = str, default = "assistant", help = "系统提示内容文件名")

args = parser.parse_args()
inputs = args.inputs
if not inputs:
    raise SystemExit

apiKey = args.apikey
for prompt_path_i in (args.prompt, PROMPT_PATH+args.prompt):
    if os.path.exists(prompt_path_i) and os.path.isfile(prompt_path_i):
        with open(prompt_path_i, 'r', encoding = "utf-8") as rf:
            system_prompt = rf.read()
        break
else:
    myWarning(f"系统提示内容不存在 : {args.prompt}")
    system_prompt = ""

client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")

def showTokens(usage):
    print("\n\n"+"="*10)
    print(f"- total tokens : {usage.total_tokens} ({usage.completion_tokens} + {usage.prompt_tokens})")
    print(f"- prompt tokens (hit+miss) : {usage.prompt_tokens} ({usage.prompt_cache_hit_tokens} + {usage.prompt_cache_miss_tokens})")
    if usage.completion_tokens_details:
        print(f"completion tokens details: {usage.completion_tokens_details}")
    if usage.prompt_tokens_details:
        print(f"prompt tokens details: {usage.prompt_tokens_details}")
    print("="*10+"\n")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": inputs},
    ],
    stream=True
)

for res in response:
    print(res.choices[0].delta.content, end = '', flush = True)
showTokens(res.usage)


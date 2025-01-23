#!/usr/bin/python
from openai import OpenAI
from argparse import ArgumentParser
import json
import os

# CONSTANTS
SCIPT_PATH = os.path.dirname(__file__)
PROMPT_PATH = SCIPT_PATH+"/../assets/prompts/"
with open(SCIPT_PATH+"/config.json", 'r', encoding = "utf-8") as rf:
    deepseek = json.load(rf)

def myWarning(info: str):
    print(f"\033[93mWarning: {info}\033[0m")

parser = ArgumentParser(description = "vim-deepseek ask")
parser.add_argument("inputs", type = str, default="", help = "输入")
parser.add_argument("-k", "--apikey", type = str, default = "", help = "apikey")
parser.add_argument("-m", "--model", type = str, default = deepseek["model_default"], help = "模型 (dsV3 / dsR1)")
parser.add_argument("-p", "--prompt", type = str, default = "assistant", help = "系统提示内容文件名")

args = parser.parse_args()
inputs = args.inputs
if not inputs:
    raise SystemExit

model_select = args.model
apiKey = args.apikey
for prompt_path_i in (args.prompt, PROMPT_PATH+args.prompt):
    if os.path.exists(prompt_path_i) and os.path.isfile(prompt_path_i):
        with open(prompt_path_i, 'r', encoding = "utf-8") as rf:
            system_prompt = rf.read()
        break
else:
    myWarning(f"系统提示内容不存在 : {args.prompt}")
    system_prompt = ""

def showTokens(usage):
    print("\n\n"+"="*10)
    print(f"- total tokens : {usage.total_tokens} ({usage.completion_tokens} + {usage.prompt_tokens})")
    print(f"- prompt tokens (hit+miss) : {usage.prompt_tokens} ({usage.prompt_cache_hit_tokens} + {usage.prompt_cache_miss_tokens})")
    if usage.completion_tokens_details:
        print(f"completion tokens details: {usage.completion_tokens_details}")
    if usage.prompt_tokens_details:
        print(f"prompt tokens details: {usage.prompt_tokens_details}")
    print("="*10+"\n")

client = OpenAI(api_key = apiKey, base_url = deepseek["api_url"])

if __name__ == "__main__":
    response = client.chat.completions.create(
        model = deepseek["models"][model_select],
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": inputs},
        ],
        stream=True
    )

    have_reason = False
    start_reason = True
    for res in response:
        try:
            res_reason_content = res.choices[0].delta.reasoning_content
            if res_reason_content:
                have_reason = True
                if start_reason:
                    print("=== THINK START ===\n")
                    start_reason = False
                response_reason_contents += res_reason_content
                print(res_reason_content, end = '', flush = True)
        except:
            have_reason = False
        res_content = res.choices[0].delta.content
        if res_content:
            if have_reason:
                print("\n\n=== THINK END ===\n\n")
                have_reason = False
            print(res_content, end = '', flush = True)
    showTokens(res.usage)


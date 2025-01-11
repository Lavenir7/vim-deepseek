from argparse import ArgumentParser
from yaml import dump, safe_load
import os

# CONSTANTS
SCIPT_PATH = os.path.dirname(__file__)
CHATS_PATH = SCIPT_PATH+"/../assets/chats/"
CHAT_LIST_PATH = CHATS_PATH+".list.yml"
# params
parser = ArgumentParser(description = "Delete session file")
parser.add_argument("session", type=str, help="会话编号")
args = parser.parse_args()

def myWarning(info: str):
    print(f"\033[93mWarning: {info}\033[0m")

if __name__ == "__main__":
    chat_name = f"chat_{args.session}"
    if os.path.exists(CHAT_LIST_PATH) and os.path.isfile(CHAT_LIST_PATH):
        with open(CHAT_LIST_PATH, 'r', encoding = "utf-8") as rf:
            chat_list = safe_load(rf.read())
            if not chat_list:
                chat_list = dict()
    else:
        chat_list = dict()
    if chat_name not in chat_list.keys():
        myWarning(f"会话 {chat_name} 不存在")
    del chat_list[chat_name]
    with open(CHAT_LIST_PATH, 'w', encoding = "utf-8") as wf:
        wf.write(dump(chat_list))
    chat_file_path = CHATS_PATH+chat_name+".yaml"
    try:
        os.remove(chat_file_path)
        # print(f"已删除会话: {chat_name}")
    except FileNotFoundError:
        myWarning(f"会话文件 {chat_file_path} 不存在 ({chat_name}已从会话列表中移除)")
    except PermissionError:
        myWarning(f"无权限删除会话文件 {chat_file_path}, 请尝试手动删除 ({chat_name}已从会话列表中移除)")
    except Exception as e:
        myWarning(f"删除会话文件 {chat_file_path} 时发生错误 ({chat_name}已从会话列表中移除) : {e}")

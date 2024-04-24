import json
import sys


instruct_dict = {"de": "German", "en": "English", "zh": "Chinese"}

lang = sys.argv[1]
sl = lang[:2]
tl = lang[-2:]

dir_path = sys.argv[2]

wmt_path = sys.argv[3]
src_file = open(wmt_path, 'r')
src_list = [line.strip() for line in src_file]

prompt_list = []
for src in src_list:
    prompt_dict = dict()
    prompt_dict["instruction"] = f"Translate from {instruct_dict[sl]} to {instruct_dict[tl]}."
    prompt_dict["input"] = src
    prompt_dict["output"] = ""
    prompt_dict["draft"] = ""

    prompt_list.append(prompt_dict)

out_file = open(f"{dir_path}/prompt.newstest22.{lang}.{sl}.json", 'w')
json.dump(prompt_list, out_file, ensure_ascii=False, indent=4)

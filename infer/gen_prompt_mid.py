import json
import sys


instruct_dict = {"de": "German", "en": "English", "zh": "Chinese"}

lang = sys.argv[1]
sl = lang[:2]
tl = lang[-2:]

dir_path = sys.argv[2]
quality_type = sys.argv[3]

wmt_path = sys.argv[4]
src_file = open(wmt_path, 'r')
src_list = [line.strip() for line in src_file]

prompt_list = []
for src in src_list:
    prompt_dict = dict()
    if quality_type == "label":
        prompt_dict["instruction"] = "Translate from {0} to {1}, " \
                                     "and label the translation quality as \"Good\", \"Medium\" or \"Bad\".".format(instruct_dict[sl], instruct_dict[tl])
    else:
        prompt_dict["instruction"] = "Translate from {0} to {1}, " \
                                     "and score the translation quality from 0 to 100.".format(instruct_dict[sl], instruct_dict[tl])
    prompt_dict["input"] = src
    prompt_dict["output"] = ""
    prompt_dict["draft"] = ""

    prompt_list.append(prompt_dict)

out_file = open("{0}/mid/prompt.newstest22.{1}.{2}.json".format(dir_path, lang, sl), 'w')
json.dump(prompt_list, out_file, ensure_ascii=False, indent=4)

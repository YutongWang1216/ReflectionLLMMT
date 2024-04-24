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

ref_file = open("{0}/mid/{1}/hyp.txt".format(dir_path, lang), 'r')
ref_list = [line.strip() for line in ref_file]

label_file = open("{0}/mid/{1}/label.txt".format(dir_path, lang), 'r')
label_list = [line.strip() for line in label_file]

print(len(src_list) == len(ref_list), (len(src_list), len(ref_list)))
print(len(src_list) == len(label_list), (len(src_list), len(label_list)))

prompt_list = []
for src, label, ref in zip(src_list, label_list, ref_list):
    if len(ref) > 500:
        ref = ref[:500]
        if quality_type == "label":
            label = "Bad"
        else:
            label = "40"
    prompt_dict = dict()
    prompt_dict["instruction"] = "Translate from {0} to {1}.".format(instruct_dict[sl], instruct_dict[tl])
    prompt_dict["input"] = src
    prompt_dict["output"] = ""
    if quality_type == "label":
        prompt_dict["draft"] = "Draft with quality label:\n" \
                               "[{0}] {1}\n\n### Note: A translation without errors could be.".format(label, ref)
    else:
        prompt_dict["draft"] = "Draft with quality score:\n" \
                               "[{0}] {1}\n\n### Note: A translation without errors could be.".format(label, ref)
    prompt_list.append(prompt_dict)

out_file = open("{0}/final/prompt.newstest22.{1}.{2}.json".format(dir_path, lang, sl), 'w')
json.dump(prompt_list, out_file, ensure_ascii=False, indent=4)

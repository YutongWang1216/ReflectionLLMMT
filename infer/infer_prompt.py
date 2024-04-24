#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import os
import sys
import argparse
import torch



lang_instruction = {'de': "German", 'en': "English", 'ja': "Japanese", 'zh': "Chinese"}

PROMPT_DICT = {
    "prompt_input": (
        "Write a response that appropriately completes the request.\n\n"
        "### Request:\n{instruction}\n{input}\n\n### Response:"
    ),
    "prompt_no_input": (
        "Write a response that appropriately completes the request.\n\n"
        "### Request:\n{instruction}\n\n### Response:"
    ),
    "prompt_draft": (
        "Write a response that appropriately completes the request.\n\n"
        "### Request:\n{instruction}\n{input}\n\n### Hint:\n{draft}\n\n### Response:"
    ),
}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

cnt = 0

from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline


def post_processing(text):
    replace_words = ["#PR_SORG#", "#PRS=ORG#", "#PRS_ORG#_ORG#", "#PRS_MUSIC#", "#PURO_BOX#", "#PRS_SIGNUP#", "#prs_org#",
                     "#PERS_ACC#", "#PRS-ORG#", "##PRS_ORG##", "#PRI_ORG", "PRS _ORG#", "PRS.ORG#", "#PRS _ ORG#",
                      "#PROS#", "#PRS_SIG#", "#PRS_CHI#", "PRS_#",
                     "#PR_SYS#", "#PERSO#", "#PrsOrg#", "ＰＲＳＯＧＥ", "PRS ORG", "#PR_SIG#", "#PRS__ORG#", "#PRS_#ORG#", "#PRS_ORG##"]

    for word in replace_words:
        if word in text:
            text = text.replace(word, "#PRS_ORG#")

    if "#PRS" in text:
        text = text.replace("#PRS", "#PRS_ORG#").replace("#PRS_ORG#_ORG#", "#PRS_ORG#")

    return text


def func(text):

    global cnt
    if cnt == 0:
        print(text)
        sys.stdout.flush()
        cnt += 1

    hyp = pipeline(text,
                   temperature=0.1,
                   top_p=0.9,
                   do_sample=False,
                   num_beams=4,
                   max_new_tokens=256,
                   no_repeat_ngram_size=15,
                   pad_token_id=tokenizer.pad_token_id,
                   eos_token_id=tokenizer.eos_token_id)[0]["generated_text"]


    hyp = hyp.strip().replace("\n", "\\n")

    return post_processing(hyp)


def init_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", default=".",  type=str)
    parser.add_argument("-i", "--input_file", help="name of the input file")
    parser.add_argument("-o", "--output_file", help="name of the output file", type=str)
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("--each", type=int)
    parser.add_argument("--idx", type=int)

    return parser


if __name__ == '__main__':
    arg_parser = init_opt()

    args = arg_parser.parse_args()

    modelpath = args.model_path
    infile = args.input_file
    outfile = args.output_file

    lang = args.lang
    sl = lang[:2]
    tl = lang[-2:]

    step = args.each
    idx = args.idx

    tokenizer = AutoTokenizer.from_pretrained(modelpath, cache_dir=modelpath)

    model = AutoModelForCausalLM.from_pretrained(modelpath, torch_dtype=torch.float16,
                                                 cache_dir=modelpath, low_cpu_mem_usage=True).cuda()

    pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer,
                                      return_full_text=False, device=model.device,
                                      clean_up_tokenization_spaces=False,
                                      handle_long_generation="hole"
                                      )

    inf = open(infile, "r")
    outf = open(outfile, "w")

    NUM=0

    data = json.load(inf)
    prompt_data = data[step * idx: step * (idx + 1)]

    for prompt_dict in prompt_data:

        if prompt_dict.get("draft", "") != "":
            prompt_template = PROMPT_DICT["prompt_draft"]
        elif prompt_dict.get("input", "") != "":
            prompt_template = PROMPT_DICT["prompt_input"]
        else:
            prompt_template = PROMPT_DICT["prompt_no_input"]

        prompt = prompt_template.format_map(prompt_dict)

        trans = func(prompt)

        outf.write(trans+"\n")
        NUM += 1
        if NUM % 10 == 0:
            print(f"###Processing {NUM} examples.")
            outf.flush()
            sys.stdout.flush()

    inf.close()
    outf.close()


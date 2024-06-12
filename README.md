# ReflectionLLMMT

<div align="center">
    <img src="images/logo.png" width=250></img>
    <p class="image-caption">TasTe: Teaching Large Language Models to Translate through Self-Reflection</p>
</div>

## **📣 News**

- **[24/04/2024] Our code and dataset for TasTe is released!**
- **[15/05/2024] Our paper is accepted by [ACL 2024](https://2024.aclweb.org/) main conference!**


## **🔗 Quick Links**

- **[About TasTe](#about)**
- **[File Structure](#structure)**
- **[Requirements](#requirements)**
- **[Quick Start](#start)**
- **[Citation](#citation)**


## **🤖 About TasTe**<a name="about"></a>
The **TasTe** framework, which is short for **Teaching Large Language Models to Translate through Self-Reflection**, is designed as a two-stage inference process to enhance the translation quality of MT-LLMs. It consists of the following two stages:

- **Stage 1**: Generate preliminary translations (i.e. drafts) and conduct self-assessment of the translation quality at the same time.
- **Stage 2**: Refine the preliminary translations according to the predicted quality levels to obtain final outputs.

To ensure the sufficient capability for the entire self-reflective translation process, the LLMs are fine-tuned on a multi-task training set. The dataset consists of three parts:

- **Basic Translation**: Common parallel corpus to provide the LLMs with correct multilingual knowledge.
- **Quality Prediction**: Sources and translation candidates with their evaluated COMET scores to equip the LLMs with knowldge about translation quality and capabilities to make translation assessments.
- **Draft Refinement**: Preliminary translations with their COMET scores and enhanced translations to teach the LLMs to refine drafts according to their quality scores.

<div align="center">
    <img src="images/framework.png"></img>
    <p class="image-caption">The Framework of TasTe</p>
</div>


## **📜 File Structure**<a name="structure"></a>
| Directory      | Contents                     |
| -------------- | ---------------------------- |
| [`checkpoints/`](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/checkpoints) | Fine-tuned model checkpoints |
| [`data/`](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/data)        | Experimental Data            |
| [`infer/`](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/infer)       | Testing scripts              |
| [`results/`](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/results)     | Testing outputs              |
| [`train/`](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/train)       | Fine-tuning scripts          |


## **🛠️ Requirements**<a name="requirements"></a>
TasTe is developed with [HuggingFaces's transformers](https://github.com/huggingface/transformers) and [Deepspeed-chat](https://github.com/microsoft/DeepSpeedExamples/tree/master/applications/DeepSpeed-Chat).
- Python 3.7.9
- Pytorch 1.13.1+cu111
- Transformers==4.28
- accelerate==0.19.0
- numpy==1.21.6
- deepspeed==0.9.0
- scikit-learn
- flash-attn

## **🚀 Quick Start**<a name="start"></a>

### **Installation**

```bash
git clone https://github.com/YutongWang1216/ReflectionLLMMT.git
cd ReflectionLLMMT
pip install -r requirments.txt
pip install flash-attn --no-build-isolation
```

### **Fine-tuning for TasTe models**

(1) **FixEmb**: Tuning with Embedding Layers Fixed

- [train/train_fixemb.sh](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/train/train_fixemb.sh)


(2) **Full**: Tuning with Full Parameters

- [train/train_full.sh](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/train/train_full.sh)

Make sure to fill in the following parameters before running:

```bash
work_dir=/path/to/ReflectionLLMMT      # path to the ReflectionLLMMT root directory
model_name=name_of_your_model          # name your model, e.g. bloom_fixemb
settings=tc                            # training settings, choices=[tc, qe, mt]
premodel=/path/to/original/checkpoint  # path to the pretrained model checkpoint directory
GPU_NUM=8                              # number of available GPUs
GPU=0,1,2,3,4,5,6,7                    # GPU ids
```

There are three choices of training settings, corresponsing to three different training sets:

1. *tc* - Fine-tune with data in [data/train_tc.json](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/data/train_tc.json) to get a TasTe model in Text Classification style.
2. *qe* - Fine-tune with data in [data/train_qe.json](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/data/train_qe.json) to get a TasTe model in Quality Estimation style.
3. *mt* - Fine-tune with data in [data/train_mt.json](data/train_mt.json) to get a MT-baseline model.

### **Evaluating TasTe models**

- [infer/test.sh](https://github.com/YutongWang1216/ReflectionLLMMT/tree/main/infer/test.sh)

Make sure to fill in the following parameters before running:

```bash
work_dir=/path/to/ReflectionLLMMT  # path to the ReflectionLLMMT root directory
lang=zh-en                         # language pair to be tested in, choices=['zh-en', 'en-zh', 'de-en', 'en-de']
test_model=name_of_model           # name of the fine-tuned model you gave
settings=tc                        # model settings, choices=[tc, qe, mt]
GPU_NUM=8                          # number of available GPUs
```

There are also three choices of testing settings, corresponsing to three different training settings:

1. *tc* - Test a TasTe model in Text Classification style.
2. *qe* - Test a TasTe model in Quality Estimation style.
3. *mt* - Test a MT-baseline model.


## **📝 Citation**<a name="citation"></a>
If you find this repo useful, please cite our paper as:
```

```

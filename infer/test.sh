
work_dir=/path/to/ReflectionLLMMT  # path to the ReflectionLLMMT root directory
lang=zh-en  # language pair to be tested in, choices=['zh-en', 'en-zh', 'de-en', 'en-de']
test_model=name_of_model  # name of the fine-tuned model
settings=tc  # model settings, choices=[tc, qe, mt]
GPU_NUM=8  # number of available GPUs

code_dir=${work_dir}/results
TEST_PATH=${code_dir}/${test_model}
src=${lang%-*}
tgt=${lang#*-}


WMT_PATH=${work_dir}/data/newstest22.${lang}.${src}
MODEL_PATH=${work_dir}/checkpoints/${test_model}

if [ ${settings} = 'mt' ]; then
  python ${code_dir}/gen_prompt_mt.py ${lang} ${TEST_PATH} ${WMT_PATH}

  DATA_PATH=${TEST_PATH}/${lang}
  FILE_PATH=${TEST_PATH}/prompt.newstest22.${lang}.${src}.json
  bash ${code_dir}/infer_arg.sh ${DATA_PATH} ${MODEL_PATH} ${FILE_PATH} ${lang} ${GPU_NUM}

else
  if [ ! -d ${TEST_PATH} ]; then
    mkdir -p ${TEST_PATH}/mid
    mkdir -p ${TEST_PATH}/final
  fi

  if [ ${settings} = 'tc' ]; then
    quality_type=label
  else
    quality_type=score
  fi

  python ${code_dir}/gen_prompt_mid.py ${lang} ${TEST_PATH} ${quality_type} ${WMT_PATH}

  DATA_PATH=${TEST_PATH}/mid/${lang}
  if [ ! -d ${DATA_PATH} ]; then
    mkdir -p ${DATA_PATH}
  fi

  FILE_PATH=${TEST_PATH}/mid/prompt.newstest22.${lang}.${src}.json
  bash ${code_dir}/infer_arg.sh ${DATA_PATH} ${MODEL_PATH} ${FILE_PATH} ${lang} ${GPU_NUM}

  python ${code_dir}/postproc.py ${DATA_PATH} ${quality_type}
  python ${code_dir}/gen_prompt_final.py ${lang} ${TEST_PATH} ${quality_type} ${WMT_PATH}

  DATA_PATH=${TEST_PATH}/final/${lang}
  if [ ! -d ${DATA_PATH} ]; then
    mkdir -p ${DATA_PATH}
  fi

  FILE_PATH=${TEST_PATH}/final/prompt.newstest22.${lang}.${src}.json
  bash ${code_dir}/infer_arg.sh ${DATA_PATH} ${MODEL_PATH} ${FILE_PATH} ${lang} ${GPU_NUM}
fi

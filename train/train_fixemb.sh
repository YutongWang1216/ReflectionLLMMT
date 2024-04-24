
work_dir=/path/to/ReflectionLLMMT  # path to the ReflectionLLMMT root directory
model_name=name_of_your_model  # name your model, e.g. bloom_fixemb
settings=tc  # Training settings
premodel=/path/to/original/checkpoint  # path to the pretrained model checkpoint directory
GPU_NUM=8  # number of available GPUs
GPU=0,1,2,3,4,5,6,7  # GPU ids

code_dir=${work_dir}/train
data_dir=${work_dir}/data

predata=${data_dir}/demo.json
predatas=${data_dir}/train_${settings}.json
save_root_dir=${work_dir}/checkpoints

grad_step=8
batch_size=2

data_num=$(python ${data_dir}/get_len.py ${predatas})
MAX_STEPS=`expr $data_num / $GPU_NUM / $grad_step / $batch_size + 1`
SAVE_STEPS=500
EPOCHS=1
BLOCK_SIZE=768

export TRANSFORMERS_CACHE=${data_dir}/cache/
export HF_HOME=${data_dir}/cache/
export TORCH_EXTENSIONS_DIR=${data_dir}/cache/torch_extension/${model_name}
export OMP_NUM_THREADS=20
export CXX=g++

ckpt_dir=${save_root_dir}/${model_name}
LOG_FILE=${ckpt_dir}/log.${model_name}

if [ ! -d ${ckpt_dir} ]; then
    mkdir -p ${ckpt_dir}
fi


CUDA_VISIBLE_DEVICES=${GPU} deepspeed \
    ${code_dir}/run_clm_sft.py \
    --model_name_or_path ${premodel} \
    --train_file ${predata} \
    --train_files ${predatas} \
    --use_low_cpu_mem True \
    --only_optimize_layers "9" "8" "7" "6" "5" "4" "3" "2" "1" "0" \
    --rl_alpha 0.0 \
    --streaming \
    --stream_buffer_size 10000 \
    --num_train_epochs ${EPOCHS} \
    --preprocessing_num_workers 10 \
    --ignore_data_skip True \
    --warmup_ratio 0.03 \
    --keep_linebreaks False \
    --logging_steps 50 \
    --save_total_limit 5 \
    --overwrite_output_dir \
    --save_steps ${SAVE_STEPS} \
    --max_steps ${MAX_STEPS} \
    --weight_decay 0. \
    --adam_beta2 0.95 \
    --learning_rate 2e-5 \
    --block_size ${BLOCK_SIZE} \
    --gradient_accumulation_steps ${grad_step} \
    --per_device_train_batch_size ${batch_size} \
    --per_device_eval_batch_size 1 \
    --deepspeed ${data_dir}/ds_config_stage3.json \
    --cache_dir ${data_dir}/cache/ \
    --do_train \
    --fp16 \
    --output_dir ${ckpt_dir} \
2>&1 |tee ${LOG_FILE}

rm -r ${data_dir}/cache/torch_extension/${model_name}


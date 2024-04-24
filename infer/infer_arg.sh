echo ${PATH}
nvidia-smi

DATAPATH=$1
modelpathroot=$2
input_file=$3
lang=$4
GPU_NUM=$5

work_dir=/path/to/work/dir
InferCODEPATH=${work_dir}/infer
data_dir=${work_dir}/data

pyfile=infer_prompt.py

modelpath=${modelpathroot}

if [ ! -d $DATAPATH ] ; then
    mkdir -p $DATAPATH
fi

logfile=${DATAPATH}/log.out

echo "modelpath: ${modelpath}" | tee -a ${logfile}
echo "datapath: ${input_file}" | tee -a ${logfile}

tmp_dir=${DATAPATH}/tmp

if [ ! -d $tmp_dir ] ; then
    mkdir -p $tmp_dir
    chmod 777 $tmp_dir -R
fi

END=`expr $GPU_NUM - 1`
FILE_LINES=`python ${data_dir}/test_len.py ${input_file}`
EACH_LINE=`expr $FILE_LINES / $GPU_NUM + 1`

for j in $(seq 0 $END);
  do
    GPU_ID=${j}
    echo ${GPU_ID}

    CUDA_VISIBLE_DEVICES=${GPU_ID} \
    python3 -u ${InferCODEPATH}/${pyfile} \
    -i ${input_file} \
    -o ${tmp_dir}/infer0${j}.out \
    --lang ${lang} \
    --each ${EACH_LINE} --idx ${j} \
    --model_path $modelpath &

done
wait

cat ${tmp_dir}/infer*.out > ${DATAPATH}/infer.res

rm -r ${tmp_dir}

mv ${DATAPATH}/infer.res ${DATAPATH}/infer.out

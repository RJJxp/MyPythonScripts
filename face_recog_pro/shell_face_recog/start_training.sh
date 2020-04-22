#!/bin/bash
set -ue

###
# This script is to start training using the generated data.
###

# input variable
DATA_FOLDER_NAME=$1

# 01 set up dir and path
CURRENT_PATH=$(cd `dirname $0`; pwd)
echo ${CURRENT_PATH}
INSIGHTFACE_DIR=${CURRENT_PATH}/../..
SRC_DIR=${INSIGHTFACE_DIR}/src
DATASETS_DIR=${INSIGHTFACE_DIR}/datasets/${DATA_FOLDER_NAME}
MODEL_DIR=${INSIGHTFACE_DIR}/models
LOG_DIR=${INSIGHTFACE_DIR}/log

# 02 setup the parameters
pretrained_folder="id_06_th"
pretrained_keyid="0031"
model_folder="id_07_th"  # output model folder
model_name="id_07_th"    # output model name
batch_size=1024  # --per-batch-size is 64 * i
gpu_devices="0,1,2,3" # The server has 8 GTX1080-ti 

# 03 set environment variable
export MXNET_CPU_WORKER_NTHREADS=24 # The server has a 32-thread cpu and 128g RAM
export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export MXNET_ENGINE_TYPE=ThreadedEnginePerDevice

# 04 make dir of the output model
mkdir ${MODEL_DIR}/${model_folder} -p

# 05 start training
CUDA_VISIBLE_DEVICES=${gpu_devices} python -u ${SRC_DIR}/train_softmax.py --network y1 --ckpt 2 --loss-type 4 --max-steps 100000 --lr 0.001 --lr-steps 20000,30000,40000 --wd 0.00004 --fc7-wd-mult 10 --emb-size 128 --per-batch-size $((${batch_size}/4)) --margin-s 128 --data-dir ${DATASETS_DIR}/train_res --target val --verbose 1000 --pretrained ${MODEL_DIR}/${pretrained_folder}/${pretrained_folder},${pretrained_keyid} --prefix ${MODEL_DIR}/${model_folder}/${model_name} 2>&1 | tee ${LOG_DIR}/ft_rjp_log_$(date +%Y-%m-%d-%H-%M-%S).txt

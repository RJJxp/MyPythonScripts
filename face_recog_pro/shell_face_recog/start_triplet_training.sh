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
SRC_DIR=${INSIGHTFACE_DIR}/src/
DATASETS_DIR=${INSIGHTFACE_DIR}/datasets/${DATA_FOLDER_NAME}
MODEL_DIR=${INSIGHTFACE_DIR}/models
LOG_DIR=${INSIGHTFACE_DIR}/log

# 02 setup the parameters
pretrained_folder="fif_id_th"
pretrained_keyid="0012"
model_folder="triplet_01_id"  # output model folder
model_name="triplet_01_id"    # output model name
batch_size=900  # --per-batch-size is 3 * i
triplet_bag_size=1800
# --triplet-bag-size is m * batch_size
gpu_devices="0,1,2,3" # The server has 8 GTX1080-ti 

# 03 set environment variable
export MXNET_CPU_WORKER_NTHREADS=24 # The server has a 32-thread cpu and 128g RAM
export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export MXNET_ENGINE_TYPE=ThreadedEnginePerDevice

# 04 make dir of the output model
mkdir ${MODEL_DIR}/${model_folder} -p

# 05 start training
CUDA_VISIBLE_DEVICES=${gpu_devices} python -u ${SRC_DIR}/train_triplet.py --network y1 --ckpt 2 --loss-type 1 --lr 0.001 --lr-steps 20000,30000,40000 --wd 0.00004 --emb-size 128 --per-batch-size $((${batch_size}/4)) --triplet-bag-size ${triplet_bag_size} --triplet-alpha 0.5 --verbose 1000 --data-dir ${DATASETS_DIR}/train_res --target val --pretrained ${MODEL_DIR}/${pretrained_folder}/${pretrained_folder},${pretrained_keyid} --prefix ${MODEL_DIR}/${model_folder}/${model_name} 2>&1 | tee ${LOG_DIR}/finetune_log_$(date +%Y-%m-%d-%H-%M-%S).txt


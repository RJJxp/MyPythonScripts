#!/bin/bash
set -ue

###
# This script is to test the training result.
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
model_folder="fif_id_th"
model_keyid="0012"
gpu_id=0

# 03 verify the model
python -u ${SRC_DIR}/eval/verification.py --gpu ${gpu_id} --model ${MODEL_DIR}/${model_folder}/${model_folder},${model_keyid} --target test --data-dir ${DATASETS_DIR}/test_res 2>&1 | tee ${LOG_DIR}/rjp_test_log_$(date +%Y-%m-%d-%H-%M-%S).txt

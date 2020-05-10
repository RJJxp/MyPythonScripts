#!/bin/bash
set -ue

###
# This script is to start training using the slim the trained model
###

# 01 input variables
MODEL_FOLDER=$1
MODEL_KEYID=$2


# 02 setup the parameters
CURRENT_PATH=$(cd `dirname $0`; pwd)
echo ${CURRENT_PATH}
INSIGHTFACE_DIR=${CURRENT_PATH}/../..
MODEL_DIR=${INSIGHTFACE_DIR}/models

python ${INSIGHTFACE_DIR}/deploy/model_slim.py --model ${MODEL_DIR}/${MODEL_FOLDER}/${MODEL_FOLDER},${MODEL_KEYID}

#!/bin/bash
set -ue

###
# This script is to start training using the generated data.
###

# 01 setup the dir
insightface_dir=/home/rjp/tenghui_face_train/insightface
datasets_dir=${insightface_dir}/datasets/th
model_dir=${insightface_dir}/models
src_dir=${insightface_dir}/src
log_dir=${insightface_dir}/log

# 02 setup the parameters
pretrained_folder="th-arcface"
pretrained_keyid="0100"
model_folder="th-finetune"
batch_size=256  # --per-batch-size is 64 * i
gpu_devices="0" # Y7000 only has GTX-1060

# set environment variable
export MXNET_CPU_WORKER_NTHREADS=1
export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export MXNET_ENGINE_TYPE=ThreadedEnginePerDevice

# start training
CUDA_VISIBLE_DEVICES=${gpu_devices} python3 -u ${src_dir}/train_softmax.py --network y1 --ckpt 2 --loss-type 4 --lr 0.001 --lr-steps 20000,30000,40000 --wd 0.00004 --fc7-wd-mult 10 --emb-size 128 --per-batch-size $((${batch_size}/4)) --margin-s 128 --data-dir ${datasets_dir}/train_res --target val --pretrained ${model_dir}/${pretrained_folder}/${pretrained_folder},${pretrained_keyid} --prefix ${model_dir}/${model_folder}/${model_folder} 2>&1 | tee ${log_dir}/finetune_log_$(date +%Y-%m-%d-%H-%M-%S).txt

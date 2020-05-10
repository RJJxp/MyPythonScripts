#!/bin/bash
set -ue

###
# This script is to finished align and face2rec for train in the server
# In order to generate the train.idx ,train.rec using train.lst and property
# Also it will be put in the insightface/train_script/dataset
# by rjp 
###

# input variable
DATA_FOLDER_NAME=$1

# set up the dir
CURRENT_PATH=$(cd `dirname $0`; pwd)
echo ${CURRENT_PATH}
INSIGHTFACE_DIR=${CURRENT_PATH}/../..
SRC_DIR=${INSIGHTFACE_DIR}/src/
DATASETS_DIR=${INSIGHTFACE_DIR}/datasets/${DATA_FOLDER_NAME}

train_dir=${DATASETS_DIR}/train
train_aligned_dir=${DATASETS_DIR}/train_aligned
train_res_dir=${DATASETS_DIR}/train_res

# 01 align 
echo "start align"
CUDA_VISIBLE_DEVICES="0,1,2,3" python ${SRC_DIR}/align/align_lfw.py --input-dir ${train_dir} --output-dir ${train_aligned_dir} --image-size '112,112'
# rename generated lst
echo "rename lst"
mv ${train_aligned_dir}/lst ${train_aligned_dir}/train.lst
# touch property
echo "generate property"
face_id_num=$(ls ${train_aligned_dir} -l |grep "^d"|wc -l)
echo "${face_id_num},112,112" > ${train_aligned_dir}/property
# 02 face2rec
echo "face2rec2"
python ${SRC_DIR}/data/face2rec2.py ${train_aligned_dir}
# 03 copy .idx .rec .lst and property to the res folder
echo "move all the generated files to train_res"
mkdir ${train_res_dir} -p
mv ${train_aligned_dir}/train.lst ${train_res_dir}   
mv ${train_aligned_dir}/property ${train_res_dir}
mv ${train_aligned_dir}/train.idx ${train_res_dir}
mv ${train_aligned_dir}/train.rec ${train_res_dir}

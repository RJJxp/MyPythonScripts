#!/bin/bash
set -ue

###
# This script is to generate val.bin for val in the server
# First align, then generate pairs.txt, generate .bin
# Also it will be put in the insightface/train_script/dataset
# by rjp 
###

# input variable
DATA_FOLDER_NAME=$1

# set up dir and path
CURRENT_PATH=$(cd `dirname $0`; pwd)
echo ${CURRENT_PATH}
INSIGHTFACE_DIR=${CURRENT_PATH}/../..
SRC_DIR=${INSIGHTFACE_DIR}/src/
DATASETS_DIR=${INSIGHTFACE_DIR}/datasets/${DATA_FOLDER_NAME}

val_dir=${DATASETS_DIR}/val
val_aligned_dir=${DATASETS_DIR}/val_aligned
val_res_dir=${DATASETS_DIR}/val_res
train_res_dir=${DATASETS_DIR}/train_res

# 01 align the photo
echo -e "start align \n from ${val_dir} \n to ${val_aligned_dir}"
CUDA_VISIBLE_DEVICES="0,1,2,3" python ${SRC_DIR}/align/align_lfw.py --input-dir ${val_dir} --output-dir ${val_aligned_dir} --image-size '112,112'

# 02 generate pairs.txt
# remove ./lst
rm ${val_aligned_dir}/lst
# use the script by rjp in the same folder
echo -e "generating pairs.txt in \n ${val_aligned_dir}"
python rjp_gen_id_image_pairs.py --input-dir ${val_aligned_dir} --same-pair-nums 1420 --diff-pair-nums 5000

# 03 pack the data into val.bin
echo "mkdir "
mkdir ${val_res_dir} -p
echo -e "start packing data into \n ${val_res_dir}"
python ${SRC_DIR}/data/lfw2pack.py --data-dir ${val_aligned_dir} --image-size '112,112' --output ${val_res_dir}/val.bin

# 04 move pairs.txt
echo "move generated pairs.txt"
mv ${val_aligned_dir}/pairs.txt ${val_res_dir}
echo "copy val.bin from val_res to train_res"
cp ${val_res_dir}/val.bin ${train_res_dir}
echo "finished all."


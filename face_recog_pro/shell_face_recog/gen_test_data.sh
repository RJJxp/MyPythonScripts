#!/bin/bash
set -ue

###
# This script is to generate test.bin for val in the server
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

test_dir=${DATASETS_DIR}/test
test_aligned_dir=${DATASETS_DIR}/test_aligned
test_res_dir=${DATASETS_DIR}/test_res

# 01 align the photo
echo "start align \n from ${test_dir} \n to ${test_aligned_dir}"
CUDA_VISIBLE_DEVICES="0,1,2,3" python ${SRC_DIR}/align/align_lfw.py --input-dir ${test_dir} --output-dir ${test_aligned_dir} --image-size '112,112'

# 02 generate property and pairs.txt
# remove ./lst
rm ${test_aligned_dir}/lst
# generate property file in test_res
face_id_nums=$(ls ${test_aligned_dir} -l |grep "^d"|wc -l)
mkdir ${test_res_dir} -p
echo "${face_id_nums},112,112" > ${test_res_dir}/property
# use the script by rjp in the same folder
echo "generating pairs.txt in \n ${test_aligned_dir}"
python rjp_gen_id_image_pairs.py --input-dir ${test_aligned_dir} --same-pair-nums 4100 --diff-pair-nums 36000

# 03 pack the data into test.bin, generate it in the test_res
echo "start packing data into \n ${test_res_dir}"
python ${SRC_DIR}/data/lfw2pack.py --data-dir ${test_aligned_dir} --image-size '112,112' --output ${test_res_dir}/test.bin

# 04 move pairs.txt
echo "move generated pairs.txt"
mv ${test_aligned_dir}/pairs.txt ${test_res_dir}
echo "finished all."

#!/bin/bash

###
# This script is to generate pairs.txt and .bin for test
###

# set up the dir
insightface_dir=/home/rjp/tenghui_face_train/insightface
src_dir=${insightface_dir}/src
datasets_dir=${insightface_dir}/datasets/th

test_dir=${datasets_dir}/test
test_aligned_dir=${datasets_dir}/test_aligned
test_res_dir=${datasets_dir}/test_res

# 01 align the face
echo "start align the pictures"
python3 ${src_dir}/align/align_lfw.py --input-dir ${test_dir} --output-dir ${test_aligned_dir} --image-size '112,112'
# remove generated lst
rm ${test_aligned_dir}/lst
# 02 generate pairs.txt
echo "generating pairs.txt"
python3 ../rjp_gen_id_image_pairs.py --input-dir ${test_aligned_dir} --same-pair-nums 10000 --diff-pair-nums 10000
# 03 generate .bin
echo "generating .bin"
mkdir ${test_res_dir} -p
python3 ${src_dir}/data/lfw2pack.py --data-dir ${test_aligned_dir} --image-size '112,112' --output ${test_res_dir}/test.bin
# move pairs.txt to the res
mv ${test_aligned_dir}/pairs.txt ${test_res_dir}
echo "finished all."

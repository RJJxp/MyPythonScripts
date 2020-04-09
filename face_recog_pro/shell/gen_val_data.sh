#!/bin/bash

###
# this script is to finished align and generate .bin for val
###

# set up the dir
insightface_dir=/home/rjp/tenghui_face_train/insightface
src_dir=${insightface_dir}/src
datasets_dir=${insightface_dir}/datasets/th

val_dir=${datasets_dir}/val
val_aligned_dir=${datasets_dir}/val_aligned
val_res_dir=${datasets_dir}/val_res

# 01 align 
echo "start align script"
python3 ${src_dir}/align/align_lfw.py --input-dir ${val_dir} --output-dir ${val_aligned_dir} --image-size '112,112'
# remove lst
echo "remove lst"
rm ${val_aligned_dir}/lst 
# 02 generate pairs.txt
echo "generating pairs.txt"
python3 ../rjp_gen_id_image_pairs.py --input-dir ${val_aligned_dir} --same-pair-nums 10000 --diff-pair-nums 10000
# 03 generate .bin
echo "packing val.bin"
mkdir ${val_res_dir} -p
python3 ${src_dir}/data/lfw2pack.py --data-dir ${val_aligned_dir} --image-size '112,112' --output ${val_res_dir}/val.bin
# 04 move pairs.txt
echo "move pairs.txt"
mv ${val_aligned_dir}/pairs.txt ${val_res_dir}
echo "finished all."
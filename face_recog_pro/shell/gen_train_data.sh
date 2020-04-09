#!/bin/bash

###
# this script is to finished align and face2rec for train
###

# set up the dir
insightface_dir="/home/rjp/tenghui_face_train/insightface"
src_dir=${insightface_dir}/src
datasets_dir=${insightface_dir}/datasets/th

train_dir=${datasets_dir}/train
train_aligned_dir=${datasets_dir}/train_aligned
train_res_dir=${datasets_dir}/train_res

# 01 align 
python3 ${src_dir}/align/align_lfw.py --input-dir ${train_dir} --output-dir ${train_aligned_dir} --image-size '112,112'
# rename generated lst
mv ${train_aligned_dir}/lst ${train_aligned_dir}/train.lst
# touch property
face_id_num=$(ls ${train_aligned_dir} -l |grep "^d"|wc -l)
echo "${face_id_num},112,112" > ${train_aligned_dir}/property
# 02 face2rec
python3 ${src_dir}/data/face2rec2.py ${train_aligned_dir}
# 03 copy .idx .rec .lst and property to the res folder
mkdir ${train_res_dir} -p
mv ${train_aligned_dir}/train.lst ${train_res_dir}   
mv ${train_aligned_dir}/property ${train_res_dir}
mv ${train_aligned_dir}/train.idx ${train_res_dir}
mv ${train_aligned_dir}/train.rec ${train_res_dir}
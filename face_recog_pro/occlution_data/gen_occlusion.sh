#!/bin/bash
set -ue

python3 gen_occlusion.py --label-path "/home/rjp/id_data/20200411_mask_data/train/LabelTrainAll.mat" --data-dir "/home/rjp/id_data/20200411_mask_data/train/images" --output-dir "/home/rjp/id_data/20200411_mask_data/train/trim"
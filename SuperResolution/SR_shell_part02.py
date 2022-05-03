import os
from SR_class import *

# # intersection part
# input_dir01 = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_GF_resized_split"
# output_dir01 = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_GF_resized_split_common"
# input_dir02 = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_S2_split_warp"
# output_dir02 = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_S2_split_warp_common"

# # rename part
# lr_indir = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_S2_split_warp_common"
# lr_outdir = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_S2_split_warp_common_rename"
# lr_scale = 4
# hr_indir = r"G:\S2_GF_SRDATA\firstResult\GFROI_split_common"
# hr_outdir = r"G:\S2_GF_SRDATA\firstResult\GF_HR"

# NO MATCH PART
# intersection part
input_dir01 = r"G:\SR_DATASET_RJP\20200129_SUBSET2_NOMATCH\PNG_GF_resized_split"
output_dir01 = r"G:\SR_DATASET_RJP\20200129_SUBSET2_NOMATCH\PNG_GF_resized_split_common"
input_dir02 = r"G:\SR_DATASET_RJP\20200129_SUBSET2_NOMATCH\PNG_S2_split"
output_dir02 = r"G:\SR_DATASET_RJP\20200129_SUBSET2_NOMATCH\PNG_S2_split_common"

# rename part
lr_indir = r"/home/xuwh/Documents/20220427_dataset/PNG_S2_split"
lr_outdir = r"/home/xuwh/Documents/20220427_dataset/PNG_S2_split_rename"
lr_scale = 4
hr_indir = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized_split_match"
hr_outdir = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized_split_match_rename"

if __name__ == "__main__":
    # # intersection
    # img_check = ImgCheck()
    # img_check.getIntersection(input_dir01, input_dir02, output_dir01, output_dir02)
    # print(img_check.check2Folder(output_dir01, output_dir02))

    # rename 
    img_rename = ImgRename()
    img_rename.renameLR(lr_indir, lr_outdir, lr_scale)
    img_rename.renameHR(hr_indir, hr_outdir)
    print("Finished shell main.")
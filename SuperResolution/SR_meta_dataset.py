import io
import os
import sys
import numpy as np
import shutil
import cv2 as cv
import PIL.Image as pil_image

from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
from color_matcher.normalizer import Normalizer


# ##################
# script global var
# ##################
split_size = 200
split_step = 200


# ##################
# Function
# ##################

def sampleCount(length, sample_size, sample_step):
    count = (length - sample_size) * 1.0 / sample_step
    count = int(count) + 1
    return count

def splitImg(img_path):
    all_split_img = []
    img_name = os.path.basename(img_path)[:-4]
    img = cv.imread(img_path)
    img_height = np.shape(img)[0]
    img_width = np.shape(img)[1]
    h_count = sampleCount(img_height, split_size, split_step)
    w_count = sampleCount(img_width, split_size, split_step)
    print("h:%d, w:%d" %(h_count, w_count))
    for h_c in range(h_count):
        for w_c in range(w_count):
            h = h_c * split_step
            w = w_c * split_step
            sub_img = img[h:h+split_size, w:w+split_size, :]
            all_split_img.append(sub_img)
    print("finished subset img 1000.")
    return all_split_img

def splitImgFolder(input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('outdir already exists.')
    
    os.mkdir(output_dir)
    all_sub_imgs = []
    img_names = os.listdir(input_dir)
    for img_name in img_names:
        img_path = os.path.join(input_dir, img_name)
        sub_imgs = splitImg(img_path)
        for sub_img in sub_imgs:
            all_sub_imgs.append(sub_img)
    
    print(len(all_sub_imgs))
    # save `all_sub_imgs` to `output_dir`
    # rename by the idx
    for i in range(len(all_sub_imgs)):
        output_name = "%04d.png" %(i+1)
        output_path = os.path.join(output_dir, output_name)
        cv.imwrite(output_path, all_sub_imgs[i])
        print("rename %d of %d" %(i,len(all_sub_imgs)))
    
    print("finished splitImgFolder")

def mainSplitImgFolder():
    input_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231\s2_input"
    output_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231\s2_output"
    splitImgFolder(input_dir, output_dir)

def mainMultiScale():
    input_folder = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231\s2_output"
    output_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231"
    input_scale = 5.0
    scale_list = [2.0, 2.5, 4.0, 5.0]
    upsample_list = []
    for s in scale_list:
        upsample_list.append(input_scale / s)
    # upsample by bicubic 
    for us in upsample_list:
        output_folder_name = "s2_X%.1f" %(input_scale / us)
        output_folder = os.path.join(output_dir, output_folder_name)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
            print('outdir already exists.')
        os.mkdir(output_folder)
        
        img_names = os.listdir(input_folder)
        for img_name in img_names:
            img_path = os.path.join(input_folder, img_name)
            lrimg = pil_image.open(img_path).convert('RGB')
            lrimg_resized = lrimg.resize((int(lrimg.width*us), int(lrimg.height*us)), resample=pil_image.BICUBIC)
            output_img_path = os.path.join(output_folder, img_name)
            lrimg_resized.save(output_img_path)
        print("finished %s scale" %(input_scale / us))

    print("finished main Multi Scale CM...")

def mainMultiScaleCM():
    ref_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231\gf_output"
    src_parent_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231"
    output_parent_dir = r"G:\SR_DATASET_RJP\20211226_metaSR_dataset\dataset211231"
    scale_list = [2.0, 2.5, 4.0, 5.0]
    src_dirs = []
    output_dirs = []
    for s in scale_list:
        folder_name = "s2_X%.1f" %s
        folder_dir = os.path.join(src_parent_dir, folder_name)
        src_dirs.append(folder_dir)
        fn = "X%.1f" %s
        fd = os.path.join(output_parent_dir, fn)
        output_dirs.append(fd)
    
    
    for src_dir, output_dir in zip(src_dirs, output_dirs):
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print('outdir already exists.')
        os.mkdir(output_dir)

        src_img_names = os.listdir(src_dir)
        for src_img_name in src_img_names:
            src_img_path = os.path.join(src_dir, src_img_name)
            # same name in `ref_dir` and `src_dir`
            ref_img_path = os.path.join(ref_dir, src_img_name)
            img_ref = load_img_file(ref_img_path)
            img_src = load_img_file(src_img_path)
            obj = ColorMatcher(src=img_src, ref=img_ref, method="hm")
            img_res = obj.main()
            img_res = Normalizer(img_res).uint8_norm()
            output_path = os.path.join(output_dir, src_img_name)
            save_img_file(img_res, output_path) 



if __name__ == "__main__":
    mainMultiScaleCM()
    
    print("finished sr meta datasets.")
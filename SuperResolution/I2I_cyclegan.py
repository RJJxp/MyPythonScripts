import io
import os
import sys
import numpy as np
import shutil
import cv2 as cv



def checkDir(dir_to_check):
    if os.path.exists(dir_to_check):
        shutil.rmtree(dir_to_check)
        print('%s already exists.' %dir_to_check)
    os.mkdir(dir_to_check)

def splitPix2Cyc(input_dir, output_dir):
    output_opt_dir = os.path.join(output_dir, "opt")
    output_sar_dir = os.path.join(output_dir, "sar")
    checkDir(output_opt_dir)
    checkDir(output_sar_dir)
    image_names = os.listdir(input_dir)
    for image_name in image_names:
        print(image_name)
        opt_path = os.path.join(output_opt_dir, image_name)
        sar_path = os.path.join(output_sar_dir, image_name)
        img = cv.imread(os.path.join(input_dir, image_name), 1)
        assert(np.shape(img) == (256, 512, 3))
        opt_img = img[0:255, 000:255]
        sar_img = img[0:255, 256:511]
        cv.imwrite(opt_path, opt_img)
        cv.imwrite(sar_path, sar_img)

if __name__ == "__main__":
    print("start ....")
    input_dir = r"G:\RJP_SEN1-2_DATASET_cycle\opt2sar\val"
    output_dir = r"G:\RJP_SEN1-2_DATASET_cycle"

    splitPix2Cyc(input_dir, output_dir)
    print("finished...")
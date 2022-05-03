import io
import os
import sys
import numpy as np
import shutil
import cv2 as cv

def resizeImg(scale, input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('outdir already exists.')
    os.mkdir(output_dir)

    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)
        print(img_path)
        img = cv.imread(img_path)
        dim = (400, 400)
        resized_img = cv.resize(img, dim, interpolation=cv.INTER_LINEAR)

        img_name_x = img_name[:-4] + "x%d.png" %scale
        output_path = os.path.join(output_dir, img_name_x)
        cv.imwrite(output_path, resized_img)
        print("Finished %s resized" %img_name)
    print("Finished all img resized.")

if __name__ == "__main__":
    input_dir = r"/home/xuwh/RJPcode/Real-ESRGAN/datasets/0427fake/HR"
    output_dir = r"/home/xuwh/RJPcode/Real-ESRGAN/datasets/0427fake/LR"
    scale = 4
    resizeImg(scale, input_dir, output_dir)

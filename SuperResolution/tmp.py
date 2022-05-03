import cv2
import os
import random
import shutil
import numpy as np

import numpy

path = r'G:\SAR2OPT\pix2pix\results\sar2opt_pix2pix\test_latest\zhengzhou2'

lists = os.listdir(path)

fake_opt_lists = []

for i in lists:
    if "fake_B" in i:
        fake_opt_lists.append(i)


tmp_img = cv2.imread(r"../..\WHU-SEN-City\train\zhengzhou2\subset_0_of_S2B_MSIL1C_20180607T030539_N0206_R075_T49SGU_20180607T064334_resampled_reprojected_RGB.png")

image = np.zeros_like(tmp_img)

for h_c in range(0, 9):
    for w_c in range(0, 12):
        h = h_c * 256
        w = w_c * 256
        timg = cv2.imread(os.path.join(path, str(h_c * 12 + w_c) + '_fake_B.png'))
        tmp_img[h:h + 256, w:w + 256,:] = timg

cv2.imwrite(r"../..\WHU-SEN-City\train\zhengzhou2\fake.png", tmp_img)
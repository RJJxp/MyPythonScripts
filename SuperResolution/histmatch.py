import numpy as np
import matplotlib.pyplot as plt
import cv2

#将灰度数组映射为直方图字典,nums表示灰度的数量级
def arrayToHist(grayArray,nums):
    if(len(grayArray.shape) != 2):
        print("length error")
        return None
    w,h = grayArray.shape
    hist = {}
    for k in range(nums):
        hist[k] = 0
    for i in range(w):
        for j in range(h):
            if(hist.get(grayArray[i][j]) is None):
                hist[grayArray[i][j]] = 0
            hist[grayArray[i][j]] += 1
    #normalize
    n = w*h
    for key in hist.keys():
        hist[key] = float(hist[key])/n
    return hist


#直方图匹配函数，接受原始图像和目标灰度直方图
def histMatch(grayArray,h_d):
    #计算累计直方图
    tmp = 0.0
    h_acc = h_d.copy()
    for i in range(256):
        tmp += h_d[i]
        h_acc[i] = tmp

    h1 = arrayToHist(grayArray,256)
    tmp = 0.0
    h1_acc = h1.copy()
    for i in range(256):
        tmp += h1[i]
        h1_acc[i] = tmp
    #计算映射
    M = np.zeros(256)
    for i in range(256):
        idx = 0
        minv = 1
        for j in h_acc:
            if (np.fabs(h_acc[j] - h1_acc[i]) < minv):
                minv = np.fabs(h_acc[j] - h1_acc[i])
                idx = int(j)
        M[i] = idx
    des = M[grayArray]
    return des


imdir = "./hw1_s2.jpg"
imdir_match = "./hw1_s22.jpg"

#直方图匹配
#打开文件并灰度化
im_s = cv2.imread(r"../..\WHU-SEN-City\train\changsha\subset_0_of_S2B_MSIL1C_20180418T030539_N0206_R075_T49RFM_20180418T055826_resampled_reprojected_RGB.png")

im_s = np.array(im_s)
print(np.shape(im_s))
#打开文件并灰度化
im_match = cv2.imread(r"../..\WHU-SEN-City\train\changsha\fake.png")
im_match = np.array(im_match)
print(np.shape(im_match))



hist_s = arrayToHist(im_s[:, :, 0], 256)
hist_m = arrayToHist(im_match[:, :, 0], 256)
im_d1 = histMatch(im_s, hist_m)#将目标图的直方图用于给原图做均衡，也就实现了match

hist_s = arrayToHist(im_s[:, :, 1], 256)
hist_m = arrayToHist(im_match[:, :, 1], 256)
im_d2 = histMatch(im_s, hist_m)#将目标图的直方图用于给原图做均衡，也就实现了match

hist_s = arrayToHist(im_s[:, :, 2], 256)
hist_m = arrayToHist(im_match[:, :, 2], 256)
im_d3 = histMatch(im_s, hist_m)#将目标图的直方图用于给原图做均衡，也就实现了match


im_d = np.concatenate([im_d1, im_d2, im_d3], axis=2)
cv2.imread(r"../..\WHU-SEN-City\train\changsha\match.png", im_d)

import numpy as np
import cv2 as cv

if __name__ == "__main__":
    arr = np.arange(24).reshape(2, 3, 4)
    print(arr)
    for i in range(3):
        print("sum axis = %d" %i)
        print(arr.sum(axis = i))
        print("\n")
    a = arr[0, :, :]
    print(a)
    print(a - 1)

    # img = cv.imread(r"G:\WHU-SEN-City\train\changsha\subset_0_of_S2B_MSIL1C_20180418T030539_N0206_R075_T49RFM_20180418T055826_resampled_reprojected_RGB.png")
    # print(img.shape)
    sss = "5373_01_GF_0402.png"
    ddd = sss[0:7] + sss[-8:-4]
    print(ddd)
    s234 = "5373_01_S2_0101_default"
    print(s234[0:7] + s234[11:15])
    print("finished.")
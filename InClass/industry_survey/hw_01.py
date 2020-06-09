import os
import sys
import argparse
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize 

####################################
# 注意 array 和 mat 对某些运算支持不一样
# 矩阵运算一定要用 mat
####################################

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, help='Enter the croppedFace directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def readFile(input_path):
    coors = []
    with open(input_path, 'r') as f1:
        for f_line in f1.readlines():
            xyz = f_line.strip().split(",")
            coor = []
            coor.append(float(xyz[0]))
            coor.append(float(xyz[1]))
            coor.append(float(xyz[2]))
            coors.append(coor)
    print("There is %d points." %len(coors))
    np_coors = np.asarray(coors, dtype=float)
    print("finished readFile func.")
    return np_coors

def draw2DPoints(coors):
    x_cor = []
    y_cor = []
    for coor in coors:
        x_cor.append(coor[1])
        y_cor.append(coor[0])
    plt.plot(x_cor, y_cor, 'o', markersize=1, color='b')
    plt.show()
    print("finished drawXY01")

def calculatePlane(coors):
    # calculate the mean of the coors
    coor_sum = np.asarray([0, 0, 0], dtype=float)
    for coor in coors:
        coor_sum += coor
    coor_mean = coor_sum / len(coors)
    print(coor_mean)
    # calculate the Q matrix
    Q_list= [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    Q_np = np.asarray(Q_list, dtype=float)
    # centering
    coors_center = []
    for coor in coors:
        xxx = coor - coor_mean
        coors_center.append(xxx)
    coors_center_mat = np.mat(coors_center)
    print(coors_center_mat.shape)
    Q_np = coors_center_mat.transpose() * coors_center_mat
    print(Q_np)
    # svd decomposition
    U, sigma, VT = la.svd(Q_np)
    print("U %s" %U)
    print("sigma %s" %sigma)
    print("VT %s" %VT)
    a = VT[2, 0]
    b = VT[2, 1]
    c = VT[2, 2]
    d = -a * coor_mean[0] - b * coor_mean[1] - c * coor_mean[2]
    print("a: %f" %a)
    print("b: %f" %b)
    print("c: %f" %c)
    print("d: %f" %d)
    print("finished calculate plane.")
    return a, b, c, d

def project2Plane(in_coors, a, b, c, d):
    out_coors = []
    t_denominator = a * a + b * b + c * c
    for in_coor in in_coors:
        out_coor = []        
        in_x = in_coor[0]
        in_y = in_coor[1]
        in_z = in_coor[2]
        t_numerator = -(a * in_x + b * in_y + c * in_z + d)
        t = t_numerator / t_denominator
        out_x = in_x + a * t
        out_y = in_y + b * t
        out_z = in_z + c * t
        out_coor.append(out_x)
        out_coor.append(out_y)
        out_coor.append(out_z)
        out_coors.append(out_coor)
    out_coors = np.mat(out_coors)
    print("project points:")
    print(out_coors)
    print("There is %d points in out_coors" %len(out_coors))


    coors_sum = np.mat([0, 0, 0], dtype=float)
    for in_coor in in_coors:
        coors_sum += in_coor
    coors_mean = coors_sum / len(in_coors)
    print(coors_mean)
    ehh_list = [a, b, c]
    ehh_vec = np.mat(ehh_list)
    ehh_vec_norm = normalize(ehh_vec)
    ehh_vec_norm = np.mat(ehh_vec_norm)
    print(ehh_vec_norm)
    exx_list = [-coors_mean[0, 0], -coors_mean[0, 1], -d/c-coors_mean[0, 2]]
    exx_vec = np.mat(exx_list)
    exx_vec_norm = normalize(exx_vec)
    exx_vec_norm = np.mat(exx_vec_norm)
    print(exx_vec_norm)
    eyy_vec_norm = np.cross(exx_vec_norm, ehh_vec_norm)
    print(eyy_vec_norm)

    R_T_list = [[exx_vec_norm[0, 0], exx_vec_norm[0, 1], exx_vec_norm[0, 2]],
                [eyy_vec_norm[0, 0], eyy_vec_norm[0, 1], eyy_vec_norm[0, 2]],
                [ehh_vec_norm[0, 0], ehh_vec_norm[0, 1], ehh_vec_norm[0, 2]]]
    R_T_mat = np.mat(R_T_list)
    print(R_T_mat)

    xy_coors = []
    for out_coor in out_coors:
        xy_coor_mat = -R_T_mat * coors_mean.transpose() + R_T_mat * out_coor.transpose()
        xy_coor = []
        xy_coor.append(xy_coor_mat[0, 0])
        xy_coor.append(xy_coor_mat[1, 0])
        xy_coors.append(xy_coor)
    print(np.mat(xy_coors))
    print("There is %d pts in xy_coors." %len(xy_coors))
    print("finished project2Plane func.")
    return xy_coors

if __name__ == "__main__":
    args = parseArgs()
    input_path = args.input_path
    coors = readFile(input_path)
    # draw2DPoints(coors)
    a, b, c, d = calculatePlane(coors)
    xy_coors = project2Plane(coors, a, b, c, d)
    draw2DPoints(xy_coors)
    print("finished all.")
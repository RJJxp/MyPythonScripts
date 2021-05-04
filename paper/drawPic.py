import os
import sys
import argparse
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize 

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', type=str, help='Enter the dist file path.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def drawData(file_path):
    coors = []
    with open(file_path, 'r') as f1:
        for f_line in f1.readlines():
            value = float(f_line)
            coors.append(value)
    print("There is %d points." %len(coors))
    # plt.plot(coors, 'bo-', markersize=1, color='b')
    plt.plot(coors, 'bo-', markersize=5)
    plt.show()
    print("finished draw data.")

def drawAll2Data():
    receive_dir = "D:\\study\\超声波小论文\\data\\20210112\\receive\\"
    filter_dir = "D:\\study\\超声波小论文\\data\\20210112\\min3max5\\"
    for i in range(12):
        receive_file_path = receive_dir + str(i) + "_receive.txt"
        filter_file_path = filter_dir + str(i) + "_3to5.txt"
        
        f1_line_num = 0
        f2_line_num = 0
    
        with open(receive_file_path, 'r') as f1, open(filter_file_path, 'r') as f2:
            f1_line_num = len(f1.readlines())
            f2_line_num = len(f2.readlines())
            assert f1_line_num == f2_line_num

        with open(receive_file_path, 'r') as f1, open(filter_file_path, 'r') as f2:
            y1 = []
            y2 = []
            x = list(range(f1_line_num))
            for line1, line2 in zip(f1.readlines(), f2.readlines()):
                y1.append(float(line1))
                y2.append(float(line2))
            plt.plot(x, y1, color='blue', marker='o', linewidth=1, markersize=5, label='origin_%02d' % i)
            plt.plot(x, y2, color='green', marker='o', linewidth=1, markersize=5, label='filter_%02d' % i)
            plt.legend()
            plt.title('compare_%02d' % i)
            # plt.savefig("D:\\study\\超声波小论文\\data\\fig\\result" + "_%02d" %i + ".jpg", dpi=500)
            plt.show()

def draw2Data():
    receive_file_path = "D:\\study\\超声波小论文\\data\\comparasion\\1_receive.txt"
    filter_file_path = "D:\\study\\超声波小论文\\data\\comparasion\\1_3to5_modified.txt"

    f1_line_num = 0
    f2_line_num = 0

    with open(receive_file_path, 'r') as f1, open(filter_file_path, 'r') as f2:
        f1_line_num = len(f1.readlines())
        f2_line_num = len(f2.readlines())
        assert f1_line_num == f2_line_num

    with open(receive_file_path, 'r') as f1, open(filter_file_path, 'r') as f2:
        y1 = []
        y2 = []
        x = list(range(f1_line_num))
        for line1, line2 in zip(f1.readlines(), f2.readlines()):
            y1.append(float(line1))
            y2.append(float(line2))
        plt.plot(x, y1, color='blue', marker='o', linewidth=1, markersize=5, label='origin')
        plt.plot(x, y2, color='green', marker='o', linewidth=1, markersize=5, label='filter')
        plt.legend()
        plt.title("compared")
        # plt.savefig("D:\\study\\超声波小论文\\data\\fig\\result" + "_%02d" %i + ".jpg", dpi=500)
        plt.show()

def calM():
    receive_file_path = "D:\\study\\超声波小论文\\data\\comparasion\\1_receive_part.txt"
    filter_file_path = "D:\\study\\超声波小论文\\data\\comparasion\\1_3to5_part.txt"

    with open(receive_file_path, 'r') as f1:
        y1 = []
        for line1 in f1.readlines():
            y1.append(float(line1))
        print(len(y1))
        var1 = np.var(y1)
        std1 = np.std(y1)
        print("receive var: %f" %var1)
        print("receive std: %f" %std1)

    with open(filter_file_path, 'r') as f2:
        y2 = []
        for line2 in f2.readlines():
            y2.append(float(line2))
        print(len(y2))
        var2 = np.var(y2)
        std2 = np.std(y2)
        print("filter var: %f" %var2)
        print("filter std: %f" %std2)

if __name__ == "__main__": 
    # args = parseArgs()
    # file_path = args.file_path
    # drawData(file_path)
    # draw2Data()
    calM()
    print("finished python script.")
import os
import numpy as np

def generate_fake_data(in_data):
    print("**************************")
    print("input data: %s" %in_data)
    data_mat = np.mat(in_data).T
    row, col = data_mat.shape
    # print("row is %d" %row)
    # print("col is %d" %col)
    power_list = []
    extra_power = int(row / 2)
    p_i = 1.0 / (row + extra_power)
    for i in range(row-1):
        power_list.append(p_i)
    power_list.append(p_i * (extra_power + 1))
    print("power: %s" %power_list)
    power_mat = np.mat(power_list).T
    sum = data_mat.T * power_mat
    print("**************************")
    print("sum is %f" %sum)
    print("**************************")

if __name__ == "__main__":
    in_data = [
    0.678966,
    0.706552,
    0.693621,
    0.658276,
    0.471552
    ]
    generate_fake_data(in_data)
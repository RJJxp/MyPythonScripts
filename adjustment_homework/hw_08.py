import numpy as np

if __name__ == '__main__':
    # ********************************************************
    # ****************** first sub-question ******************
    # ********************************************************
    n = 5
    t = 3
    V = np.mat([[7.9],
                [-9.6],
                [-5.4],
                [-8.4],
                [14.4]])
    p = [2.4, 2.8, 4.6, 3.7, 5.2]
    P = np.mat(np.diag(p))
    mean_error = np.sqrt(V.T * P * V / (n - t))
    print('mean error is: %f' %mean_error)
    B = np.mat([[1, 0, 0],
                [-1, 1, 0],
                [0, -1, 1],
                [0, 0, -1],
                [-1, 0, 1]])
    H = B * (B.T * P * B).I * B.T * P
    print('H is:\n', H)
    h55 = H[4, 4]
    p5 = P[4, 4]
    v5 = V[4, 0]
    variable_1 = np.abs(v5) / (mean_error * np.sqrt((1 - h55) / p5))
    print('variable_1 is %f' %variable_1)
    variable_2 = v5 * v5 / (mean_error * mean_error * (1 - h55) * (n - t) / p5)
    print('variable_2 is %f' %variable_2)
    # ********************************************************
    # ****************** second sub-question *****************
    # ********************************************************
    R = np.eye(5) - H
    R_row_mean = []
    for i in range(5):
        R_row_mean.append(np.mean(R[:,i]))
    r5_mean = R_row_mean[4]
    v_mean = np.mean(V)
    r5 = R[:, 4]
    numerator = 0
    for i in range(5):
        numerator += (r5[i] - r5_mean) * (V[i] - v_mean)
    print(numerator)
    t1 = 0
    t2 = 0
    for i in range(5):
        t1 += (r5[i] - r5_mean) * (r5[i] - r5_mean)
        t2 += (V[i] - v_mean) * (V[i] - v_mean)
    denominator = np.sqrt(t1 * t2)
    print(denominator)
    variable_3 = numerator / denominator
    print(variable_3)
    
import numpy as np
import math



if __name__ == '__main__':
    print('rjp')
    x = [0, 89539.402, 89538.107, 89529.801, 89530.982]
    y = [0, 23013.739, 23017.005, 23013.882, 23010.565]
    # 1st row
    a00 = 2 * x[1] - (x[2] + x[4])
    a01 = 2 * y[1] - (y[2] + y[4])
    a02 = x[4] - x[1]
    a03 = y[4] - y[1]
    a04 = 0
    a05 = 0
    a06 = x[2] - x[1]
    a07 = y[2] - y[1]
    # 2nd row
    a10 = x[3] - x[2]
    a11 = y[3] - y[2]
    a12 = 2 * x[2] - (x[1] + x[3])
    a13 = 2 * y[2] - (y[1] + y[3])
    a14 = x[1] - x[2]
    a15 = y[1] - y[2]
    a16 = 0
    a17 = 0
    # 3rd row
    a20 = 0
    a21 = 0
    a22 = x[4] - x[3]
    a23 = y[4] - y[3]
    a24 = 2 * x[3] - (x[1] + x[4])
    a25 = 2 * y[3] - (y[1] + y[4])
    a26 = x[2] - x[3]
    a27 = y[2] - y[3]

    a0 = [a00, a01, a02, a03, a04, a05, a06, a07]
    a1 = [a10, a11, a12, a13, a14, a15, a16, a17]
    a2 = [a20, a21, a22, a23, a24, a25, a26, a27]

    A = np.mat([a0,
                a1,
                a2])
    print('A mat is')
    print(A)

    w1 = - (x[2] - x[1]) * (x[4] - x[1]) - (y[2] - y[1]) * (y[4] - y[1])
    w2 = - (x[1] - x[2]) * (x[3] - x[2]) - (y[1] - y[2]) * (y[3] - y[2])
    w3 = - (x[4] - x[3]) * (x[2] - x[3]) - (y[4] - y[3]) * (y[2] - y[3])

    W = np.mat([[w1], 
                [w2], 
                [w3]])
    print('W mat is')
    print(W)

    V = A.T * (A * A.T).I * W
    print('V mat is')
    print(V)
    # calculate the hat
    XY = []
    for i in range(1,5):
        XY.append(x[i])
        XY.append(y[i])
    XY_hat = []
    for i in range(len(XY)):
        XY_hat.append(XY[i] + V[i, 0])
    print('the result is')
    print(XY_hat)
    x_hat = [0]
    y_hat = [0]
    for i in range(int(len(XY_hat) / 2)):
        x_hat.append(XY_hat[i * 2])
        y_hat.append(XY_hat[i * 2 + 1])
    # calculate the angle of 1
    vec12 = np.array([x_hat[2]-x_hat[1], y_hat[2]-y_hat[1]])
    vec14 = np.array([x_hat[4]-x_hat[1], y_hat[4]-y_hat[1]])
    cos_angle_1 = vec12.dot(vec14) / (np.sqrt(vec12.dot(vec12)) * np.sqrt(vec14.dot(vec14)))
    vec21 = np.array([x_hat[1]-x_hat[2], y_hat[1]-y_hat[2]])
    vec23 = np.array([x_hat[3]-x_hat[2], y_hat[3]-y_hat[2]])
    cos_angle_2 = vec21.dot(vec23) / (np.sqrt(vec21.dot(vec21)) * np.sqrt(vec23.dot(vec23)))
    vec32 = np.array([x_hat[2]-x_hat[3], y_hat[2]-y_hat[3]])
    vec34 = np.array([x_hat[4]-x_hat[3], y_hat[4]-y_hat[3]])
    cos_angle_3 = vec32.dot(vec34) / (np.sqrt(vec32.dot(vec32)) * np.sqrt(vec34.dot(vec34)))
    vec43 = np.array([x_hat[3]-x_hat[4], y_hat[3]-y_hat[4]])
    vec41 = np.array([x_hat[1]-x_hat[4], y_hat[1]-y_hat[4]])
    cos_angle_4 = vec43.dot(vec41) / (np.sqrt(vec43.dot(vec43)) * np.sqrt(vec41.dot(vec41)))
    
    cos_angle = [cos_angle_1, cos_angle_2, cos_angle_3, cos_angle_4]
    angle_rad = np.arccos(cos_angle)
    angle_degree = np.degrees(angle_rad)
    print(angle_degree)
    dfasd = []
    for angle in angle_degree:
        deg = (90 - angle) * 3600
        dfasd.append(deg) 
    print(dfasd)
    
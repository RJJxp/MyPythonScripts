import numpy as np

if __name__ == '__main__':
    B = np.mat([[1, 0],
                [-1, 1],
                [0, 1],
                [0, -1]])
    Q = np.mat(np.diag([2, 1, 2, 2]))
    P = Q.I
    K = np.mat([[-1, 0],
                [0, 0],
                [-1, 0],
                [0, 1]])
    Q_lambda = np.mat([[0.6, 0.2],
                       [0.2, 0.4]])
    N = (B.T * P * B) 
    Q_xx = N.I + N.I * B.T * P * K * Q_lambda * K.T * P * B * N.I
    print('Q_xx:\n', Q_xx)
    # ***************************************
    # ********* second sub-question ********* 
    # ***************************************
    f_T = np.mat([[0, -1]])
    f_lambda_T = np.mat([[0, 1]])
    M_T = f_lambda_T - f_T * N.I * B.T * P * K
    print(M_T)
    Q_ff = f_T * N.I * f_T.T + M_T * Q_lambda * M_T.T
    print('Q_ff' ,Q_ff)
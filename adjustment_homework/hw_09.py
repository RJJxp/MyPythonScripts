import numpy as np

if __name__ == '__main__':
    # ***********************************************
    # *************** sub_question_01 ***************
    # ***********************************************
    print('********************** sub_question_01 ***********************')
    # contruct B_mat
    b0 = [0.742, 2.220, -7.149, 1.000, 0.000, 0.000, 0.000]
    b1 = [-5.344, 0.743, -7.176, 0.000, 1.000, 0.000, 0.000]
    b2 = [-0.567, 1.724, -7.881, 0.000, 0.000, 1.000, 0.000]
    b3 = [-1.474, -1.806, -1.830, 0.000, 0.000, 0.000, 1.000]
    b4 = [0.742, 2.220, -7.151, 1.000, 0.000, 0.000, 0.000]
    b5 = [-5.343, 0.740, -7.176, 0.000, 1.000, 0.000, 0.000]
    b6 = [-0.565, 1.724, -7.882, 0.000, 0.000, 1.000, 0.000]
    b7 = [-1.473, -1.807, -1.833, 0.000, 0.000, 0.000, 1.000]
    B_mat = np.mat([b0,
                    b1,
                    b2,
                    b3,
                    b4,
                    b5,
                    b6,
                    b7])
    # construct L_mat_1 and L_mat_2
    L_mat_1 = np.mat([[-94.153],
                      [-6.584],
                      [-68.683],
                      [85.292],
                      [-94.159],
                      [-6.539],
                      [-68.688],
                      [85.299]])
    L_mat_2 = np.mat([[-94.153],
                      [-6.584],
                      [-68.683],
                      [85.292],
                      [-94.159],
                      [-6.539],
                      [-68.688],
                      [85.699]])
    # calculate the X
    X_1 = (B_mat.T * B_mat).I * B_mat.T * L_mat_1
    X_2 = (B_mat.T * B_mat).I * B_mat.T * L_mat_2
    print('X1', '\n', X_1)
    print('X2', '\n', X_2)
    # ***********************************************
    # *************** sub_question_02 ***************
    # ***********************************************
    print('********************** sub_question_02 ***********************')    
    B_T_B = B_mat.T * B_mat
    print('B_T_B\n', B_T_B)
    eig_value, eig_vector = np.linalg.eig(B_T_B)
    max_eig_value = max(eig_value)
    min_eig_value = min(eig_value)
    print('max eigen value is %f, min eigen value is %f' %(max_eig_value, min_eig_value))
    cond_B = np.sqrt(max_eig_value / min_eig_value)
    print('condition is \n', cond_B)
    # ***********************************************
    # *************** sub_question_03 ***************
    # ***********************************************
    print('********************** sub_question_03 ***********************')
    U, Sigma, Vt = np.linalg.svd(B_T_B)
    V = Vt.T
    Sigma_inv = np.mat(np.diag(Sigma)).I
    Ut = U.T
    print('sigma:\n', Sigma)
    # only use the 4 eigen values and their vectors
    final_N_inv = np.mat(np.zeros((7, 7)))
    for i in range(4):
        final_N_inv += V[:,i] * Ut[i,:] / Sigma[i]
    # print(final_N_inv)
    new_x_1 = final_N_inv * B_mat.T * L_mat_1
    print('new_x_1:\n', new_x_1)
    new_x_2 = final_N_inv * B_mat.T * L_mat_2
    print('new_x_2:\n', new_x_2)


    

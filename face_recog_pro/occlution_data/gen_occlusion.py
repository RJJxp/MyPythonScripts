import os
import shutil
import sys
import scipy.io as scio
import argparse
from PIL import Image as PilImage

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-path', default='', type=str, help='Enter the label path')
    parser.add_argument('--data-dir', default='', type=str, help='Enter the input data directory')
    parser.add_argument('--output-dir', default='', type=str, help='Enter the output data directory')
    print('finished parsing args.')
    return parser.parse_args()

# meta_data[i][1][0] name of file 
# meta_data[i][2][0] the label of the pic
# for the label part, we only take one of them
# lable value 'label_train' or 'LabelTest'
def getLabel(label_path):
    # meta_data = scio.loadmat(label_path)['LabelTest'][0]  # for test.mat
    meta_data = scio.loadmat(label_path)['label_train'][0]  # for train.mat
    print (len(meta_data))

    file_names = []
    face_rec = []
    for my_data in meta_data:
        # only need the frontal angle
        # if (my_data[1][0][13] != 3):    # for test.mat  
        #     continue 
        if (my_data[2][0][16] != 3):    # for train.mat
            continue
        # file_names.append(my_data[0][0])      # for test.mat
        # face_rec.append(my_data[1][0][0:4])   # for test.mat
        file_names.append(my_data[1][0])        # for train.mat
        face_rec.append(my_data[2][0][0:4])     # for train.mat
    print("There is %d file names." %len(file_names))
    print("There is %d face rectangles" %len(face_rec))
    print ("finished getLabel.")
    return file_names, face_rec
    
def doIt(args):
    label_path = args.label_path
    data_dir = args.data_dir
    output_dir = args.output_dir

    # if the dir exists, delete it
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)
    filenames, face_rec = getLabel(label_path)
    assert len(filenames) == len(face_rec)
    m = 0
    for pic, rec in zip(filenames, face_rec):
        input_path = os.path.join(data_dir, pic)
        output_path = os.path.join(output_dir, pic)
        try:
            img = PilImage.open(input_path)
        except ValueError as e:
            print (e)
            print(input_path)
        # print("pic is %s, rec is %s" %(pic, rec))
        cropped = img.crop((rec[0], rec[1], int(rec[0])+int(rec[2]), int(rec[1])+int(rec[3])))
        cropped = cropped.convert('RGB')
        cropped.save(output_path)
        m += 1
        if (m%1000 == 0):
            print("+1000")
    print ("generated %d pic in output" % len(os.listdir(output_dir)))
    print ("finished doIt function.")

if __name__ == "__main__":
    args = getArgs()
    doIt(args)
    # getLabel(args.label_path)

    print ("finished all.")

# test.mat

# {'LabelTest': array([[(array(['test_00000001.jpg'], dtype='<U17'), array([[2694, 1211,  353,  353,    1,    9,  105,  144,  337,    2,    3,
#            2,    2,    1,   -1,   -1,   -1,   -1],
#        [1754, 1449,   68,   68,    3,   -1,   -1,   -1,   -1,   -1,   -1,
#           -1,   -1,   -1,   -1,   -1,   -1,   -1]], dtype=int16)),
#         (array(['test_00000002.jpg'], dtype='<U17'), array([[113,  95, 226, 226,   1,   9,  71, 181, 221,   1,   3,   1,   2,
#           3,  -1,  -1,  -1,  -1]], dtype=int16)),
#         (array(['test_00000003.jpg'], dtype='<U17'), array([[352, 114, 151, 151,   1,  17,  45, 137, 135,   1,   3,   2,   2,
#           3,  -1,  -1,  -1,  -1],
#        [799, 217, 139, 139,   2,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
#          -1,  -1,  -1,  -1,  -1]], dtype=int16)),
#         ...,
#         (array(['test_00004933.jpg'], dtype='<U17'), array([[ 80, 121, 245, 245,   1,  50,  81, 238, 242,   1,   3,   2,   2,
#           3,  -1,  -1,  -1,  -1]], dtype=int16)),
#         (array(['test_00004934.jpg'], dtype='<U17'), array([[148, 266, 276, 276,   1,  38,  68, 265, 248,   1,   3,   2,   2,
#           3,  -1,  -1,  -1,  -1]], dtype=int16)),
#         (array(['test_00004935.jpg'], dtype='<U17'), array([[110,  98, 318, 318,   1,  73, 124, 313, 302,   1,   3,   2,   2,
#           3,  -1,  -1,  -1,  -1]], dtype=int16))]],
#       dtype=[('name', 'O'), ('label', 'O')]), '__globals__': [], '__version__': '1.0', '__header__': b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Tue Sep 05 01:07:53 2017'}


# train.mat
    # {'__globals__': [], '__header__': b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Mon Oct 02 03:29:06 2017', '__version__': '1.0', '__function_workspace__': array([[ 0,  1, 73, ...,  0,  0,  0]], dtype=uint8), 'None': MatlabOpaque([(b'label_train1', b'MCOS', b'table', array([[3707764736],
    #    [         2],
    #    [         1],
    #    [         1],
    #    [         1],
    #    [         1]], dtype=uint32))],
    #          dtype=[('s0', 'O'), ('s1', 'O'), ('s2', 'O'), ('arr', 'O')]), 'label_train': array([[(array(['add_1.jpg'], dtype='<U9'), array(['train_00000001.jpg'], dtype='<U18'), array([[ 95, 160,  91,  91, 113, 177, 158, 172,   7,  26,  82,  89,   1,
    #       3,   1,   1,   3,  -1,  -1,  -1,  -1]], dtype=int16)),
    #     (array(['add_10.jpg'], dtype='<U10'), array(['train_00000002.jpg'], dtype='<U18'), array([[107,  82,  66,  66, 129,  95, 156,  96,   5,  17,  65,  56,   2,
    #       3,   1,   1,   3,  -1,  -1,  -1,  -1]], dtype=int16)),
    #     (array(['add_11.jpg'], dtype='<U10'), array(['train_00000003.jpg'], dtype='<U18'), array([[ 56, 170, 185, 185, 140, 198, 196, 208,  41,  56, 147, 182,   1,
    #       3,   1,   1,   4,  -1,  -1,  -1,  -1]], dtype=int16)),
    #     ...,
    #     (array(['weibo_997.jpg'], dtype='<U13'), array(['train_00025874.jpg'], dtype='<U18'), array([[14, 28, 83, 83, 33, 51, 72, 56,  4, 53, 80, 87,  2,  2,  2,  2,
    #      3, -1, -1, -1, -1]], dtype=int16)),
    #     (array(['weibo_998.jpg'], dtype='<U13'), array(['train_00025875.jpg'], dtype='<U18'), array([[38,  4, 72, 72, 60, 23, 93, 21,  2, 29, 65, 77,  2,  3,  2,  2,
    #      3, -1, -1, -1, -1]], dtype=int16)),
    #     (array(['weibo_999.jpg'], dtype='<U13'), array(['train_00025876.jpg'], dtype='<U18'), array([[ 72,  16,  34,  34,  79,  26,  96,  26,   4,  15,  32,  36,   2,
    #       3,   1,   2,   3,  76,  20, 104,  31]], dtype=uint8))]],
    #   dtype=[('orgImgName', 'O'), ('imgName', 'O'), ('label', 'O')])}
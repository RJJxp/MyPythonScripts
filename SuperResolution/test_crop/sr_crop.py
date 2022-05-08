import cv2
import os
import numpy as np

class MyRec:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    def __init__(self) -> None:
        pass
    
# in crop_param_file
# every line: x1, y1, x2, y2. 
# x1, y1 for leftup corner; x2, y2 for rightdown corner
# the coordinates from groudtruth image 
def readCropParam(param_file_path):
    params = []
    with open(param_file_path, 'r') as f1:
        params.append(f1.readline().strip())
        params.append(f1.readline().strip())
        params.append(f1.readline().strip())        
        for param_line in f1.readlines():
            coor4 = param_line.strip().split()
            assert(len(coor4) == 4)
            param = MyRec()
            param.x1 = coor4[0]
            param.y1 = coor4[1]
            param.x2 = coor4[2]
            param.y2 = coor4[3]
            params.append(param)
    return params

# crop the img from coor
def cropOnImgAndSave(img_path, coor_params):
    output_dir = os.path.dirname(img_path)
    output_dir = os.path.join(output_dir, os.path.basename(img_path)[0:7])
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    count_n = 0
    img = cv2.imread(img_path)
    print(img_path)
    for i in range(len(coor_params)):
        x1 = int(coor_params[i].x1)
        y1 = int(coor_params[i].y1)
        x2 = int(coor_params[i].x2)
        y2 = int(coor_params[i].y2)
        img_subset = img[x1:x2, y1:y2]
        count_n = count_n + 1
        output_name = os.path.basename(img_path)[:-4] \
                    + "_%03d_" %count_n \
                    + os.path.basename(img_path)[-4:]
        output_path = os.path.join(output_dir, output_name)
        cv2.imwrite(output_path, img_subset)
        print("save %s" %output_path)
    print("\n")

def cropOnAllImg(params):
    img_bc_path = str(params[0])
    img_sr_path = str(params[1])
    img_gt_path = str(params[2])
    coor_params = params[3:]
    cropOnImgAndSave(img_bc_path, coor_params)
    cropOnImgAndSave(img_sr_path, coor_params)
    cropOnImgAndSave(img_gt_path, coor_params)
    print("finished crop all...")

if __name__ == "__main__":
    param_file_path = r"D:\RJP_stuff\20211213_srtestdata\sr_crop_param.txt"
    params = readCropParam(param_file_path)
    print(params[3].x1)
    cropOnAllImg(params)



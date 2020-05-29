import os
import sys
import argparse
import shutil
import random

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the data directory.')
    parser.add_argument('--min-threshold', type=int, help='less than min-thre, delete the folder.')
    parser.add_argument('--max-threshold', type=int, help='more than min-thre, take part of the pics of the folder')
    parser.add_argument('--keep-threshold', type=int, help='more than min-thre, the number of pics we keep')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def cleanData(input_dir, min_t, max_t, keep_t):
    all_folders = os.listdir(input_dir)
    all_floders_num = len(all_folders)
    count = 0
    min_count = 0
    max_count = 0
    for folder in all_folders:
        folder_dir = os.path.join(input_dir, folder)
        folder_pics = os.listdir(folder_dir)
        folder_pics_num = len(folder_pics)
        if (folder_pics_num < min_t):   # if the pics'number is less than min threshold, then rm the folder
            shutil.rmtree(folder_dir)
            min_count += 1
        elif (folder_pics_num > max_t): # if the pics' number is more than max threshold, the pick part of the pics
            delete_num = folder_pics_num - keep_t   
            delete_pics = random.sample(folder_pics, delete_num)
            for delete_pic in delete_pics:
                delete_pic_path = os.path.join(folder_dir, delete_pic)
                os.remove(delete_pic_path)
            max_count += 1
        else:   # when the pics' number is what we want, do nothing
            count += 1
            # print("%d of %d" %(count, all_floders_num))
            continue
        count += 1
        # print("%d of %d" %(count, all_floders_num))
    print("There is %d folders has too many pics." %max_count)
    print("There is %d folders has too few pics." %min_count)
    print("finished clear data.")

if __name__ == "__main__":
    args = parseArgs()
    input_dir = args.input_dir
    min_t = args.min_threshold
    max_t = args.max_threshold
    keep_t = args.keep_threshold
    cleanData(input_dir, min_t, max_t, keep_t)
    print("finished all.")
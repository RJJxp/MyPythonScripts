import os
import sys
import imageio
import argparse
import time
import random
import shutil

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the idcard directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def checkIt(input_dir):
    all_guys_folder = os.listdir(input_dir)
    print(len(all_guys_folder))
    precise_count = 0
    general_count = 0
    time1 = time.time()
    fp = open('/home/rjp/Desktop/error_record_2.txt', 'w')
    for guy_folder in all_guys_folder:
        precise_count += 1
        # process input 
        guy_folder_dir = os.path.join(input_dir, guy_folder)
        guy_pics = os.listdir(guy_folder_dir)
        if len(guy_pics) != 2:
            print('!!!!!!')
            fp.writelines(guy_folder_dir + '\n')
        
        if precise_count >= 1000:
            general_count += 1
            precise_count = 0
            time2 = time.time()
            print('No %d used time %f' %(general_count * 1000, time2 - time1))
    fp.close()

if __name__ == '__main__':
    args = getArgs()
    input_dir = args.input_dir
    checkIt(input_dir)
    print('finished all.')
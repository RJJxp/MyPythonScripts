# This script is started at 2020-04-02, 18:10:03
# To regenerate the lfw training data

import os
import sys
import argparse
import time
import random
import shutil

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the croppedFace directory.')
    parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

# handle folder `croppedFace_and_RGB`
def doThis(input_dir, output_dir):
    # if the dir exists, delete it
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)
    
    person_folders = os.listdir(input_dir)
    for person_folder in person_folders:
        # mkdir output_path
        os.mkdir(os.path.join(output_dir, person_folder))
        # 
        person_path = os.path.join(input_dir, person_folder)
        person_pics = os.listdir(person_path)
        if len(person_pics) != 2:
            print(person_path)
        else:
            for person_pic in person_pics:
                if (person_pic[-7:-4] == "RGB"): # person picture
                    input_path = os.path.join(person_path, person_pic)
                    t_file_name = person_folder + "_0002.jpg"
                    output_path = os.path.join(output_dir, person_folder, t_file_name)
                    shutil.copy(input_path, output_path)
                else:   # person idcard picture
                    input_path = os.path.join(person_path, person_pic)
                    t_file_name = person_folder + "_0001.jpg"
                    output_path = os.path.join(output_dir, person_folder, t_file_name)
                    shutil.copy(input_path, output_path)
    print ("finished doThis function.")
    
# handle folder `test_data`
def do_testData(input_dir, output_dir):
    # if the dir exists, delete it
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)
    
    person_folders = os.listdir(input_dir)
    for person_folder in person_folders:
        # mkdir output_path
        os.mkdir(os.path.join(output_dir, person_folder))
        # start picking
        person_path = os.path.join(input_dir, person_folder)
        person_pics = os.listdir(person_path)
        for person_pic in person_pics:
            if (person_pic[-7:-4] == "RGB"): # person picture
                input_path = os.path.join(person_path, person_pic)
                t_file_name = person_folder + "_0002.jpg"
                output_path = os.path.join(output_dir, person_folder, t_file_name)
                shutil.copy(input_path, output_path)
            elif(person_pic[-8:-4] == "Face"):   # person idcard picture
                input_path = os.path.join(person_path, person_pic)
                t_file_name = person_folder + "_0001.jpg"
                output_path = os.path.join(output_dir, person_folder, t_file_name)
                shutil.copy(input_path, output_path)
            elif(person_pic[-9:-4] == "Front"):   # person idcard picture
                # do nothing
                continue
            else:
                print(person_folder)
    print("finished do_testData function.")

def test(input_dir):
    person_folders = os.listdir(input_dir)
    for person_folder in person_folders:
        person_path = os.path.join(input_dir, person_folder)
        person_pics = os.listdir(person_path)
        if(len(person_pics) == 1):
            print("1, %s"%person_folder) 
        elif(len(person_pics) == 3):
            print("3, %s"%person_folder)
        else:
            continue

if __name__ == '__main__':
    # parse the args
    args = parseArgs()
    input_dir = args.input_dir
    output_dir = args.output_dir
    # doThis(input_dir, output_dir)
    # do_testData(input_dir, output_dir)
    test(input_dir)
    print ('finished all')


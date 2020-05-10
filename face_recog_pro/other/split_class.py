# This script is started at 2020-04-10, 11:52
# To split the lfw data into train val and test

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
    parser.add_argument('--train-num', type=int, help="number of pairs for train")
    parser.add_argument('--val-num', type=int, help="number of pairs for val")
    parser.add_argument('--test-num', type=int, help="number of pairs for test")
    args = parser.parse_args()
    print ("parse args complete")
    return args

def splitData(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    train_num = args.train_num
    val_num = args.val_num
    test_num = args.test_num

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)

    person_folders = os.listdir(input_dir)
    print ("there is %d folders" % len(person_folders))
    persons4train = random.sample(person_folders, train_num)
    for p4train in persons4train:
        copyfrom_dir = os.path.join(input_dir, p4train)
        copyto_dir = os.path.join(output_dir, "train", p4train)
        shutil.move(copyfrom_dir, copyto_dir)
    print ("finished moving train set")

    person_folders = os.listdir(input_dir)
    persons4val = random.sample(person_folders, val_num)
    for p4val in persons4val:
        copyfrom_dir = os.path.join(input_dir, p4val)
        copyto_dir = os.path.join(output_dir, "val", p4val)
        shutil.move(copyfrom_dir, copyto_dir)
    print ("finished moving val set")

    person_folders = os.listdir(input_dir)
    persons4test = random.sample(person_folders, test_num)
    for p4test in persons4test:
        copyfrom_dir = os.path.join(input_dir, p4test)
        copyto_dir = os.path.join(output_dir, "test", p4test)
        shutil.move(copyfrom_dir, copyto_dir)
    print ("finished moving test set")

if __name__ == "__main__":
    # args
    args = parseArgs()
    
    # function
    splitData(args)
    print("finished all.")
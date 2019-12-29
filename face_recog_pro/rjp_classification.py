import os
import sys
import imageio
import argparse
import time
import random
import shutil

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the idcard directory.')
    parser.add_argument('--output-dir', type=str, help='Enter the idcard directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def moveFromTo(input_dir, output_dir):
    # judge whether the output_dir exist
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the output-dir has already exists, deleted')
    os.mkdir(output_dir)

    all_guys_folder = os.listdir(input_dir)
    for guy_folder in all_guys_folder:
        guy_path = os.path.join(input_dir, guy_folder)
        # make person's folder in output_dir
        os.mkdir(os.path.join(output_dir, guy_folder))
        all_pics = os.listdir(guy_path)
        for pic in all_pics:
            pic_path = os.path.join(guy_path, pic)
            if (pic[-8:-4] == '0001'):  # idcard
                dst_dir = os.path.join(output_dir, guy_folder, 'idcard')
                os.mkdir(dst_dir)
                dst_path = os.path.join(dst_dir, pic)
                shutil.copy(pic_path, dst_path)
            elif (pic[-8:-4] == '0002'):    # photo
                dst_dir = os.path.join(output_dir, guy_folder, 'photo')
                os.mkdir(dst_dir)
                dst_path = os.path.join(dst_dir, pic)
                shutil.copy(pic_path, dst_path)
            else:   # should do nothing
                print('shit happens  at %s' % guy_path)
                continue


if __name__ == "__main__":
    args = parseArgs()
    input_dir = args.input_dir
    output_dir = args.output_dir
    print('start moving')
    moveFromTo(input_dir, output_dir)
    print('finished all')




    
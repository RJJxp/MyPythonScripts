import os
import sys
import argparse
import shutil

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-dir', type=str, help='`person_20200508` or `person_20200527`')
    parser.add_argument('--second-dir', type=str, help='`person_20200508` or `person_20200527`')
    parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def mergeIt(second_dir, output_dir):
    total_count = 0
    duplicate_count = 0
    second_folders = os.listdir(second_dir)
    output_folders = os.listdir(output_dir)
    for second_folder in second_folders:
        if second_folder in output_folders: # duplicated, copy the neccessary file
            duplicate_count += 1
            second_folder_dir = os.path.join(second_dir, second_folder)
            second_folder_pics = os.listdir(second_folder_dir)
            output_folder_dir = os.path.join(output_dir, second_folder)
            output_folder_pics = os.listdir(output_folder_dir)
            for pic in second_folder_pics:
                if pic in output_folder_pics:   # the pic already exists, do nothing
                    continue
                else:   # the pic does not exist, copy
                    src_path = os.path.join(second_folder_dir, pic)
                    dst_path = os.path.join(output_folder_dir, pic)
                    shutil.copy(src_path, dst_path)

        else:   # not duplicated, copy the dir
            src_dir = os.path.join(second_dir, second_folder)
            dst_dir = os.path.join(output_dir, second_folder)
            shutil.copytree(src_dir, dst_dir)
        total_count += 1

    print("Total %d, duplicated %d" %(total_count, duplicate_count))
    print("finished func mergeIt.")

if __name__ == "__main__":
    args = getArgs()
    first_dir = args.first_dir
    second_dir = args.second_dir
    output_dir = args.output_dir

    # mkdir(output_dir) and copy the content of the first dir to the output dir
    shutil.copytree(first_dir, output_dir)
    mergeIt(second_dir, output_dir)

    print("finished all.")
     
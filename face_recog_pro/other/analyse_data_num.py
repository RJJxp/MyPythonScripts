import os
import sys
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the input directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

if __name__ == "__main__":
    args = parseArgs()
    input_dir = args.input_dir
    all_folders = os.listdir(input_dir)
    folder_num = len(all_folders)
    pic_num = 0
    for folder in all_folders:
        folder_path = os.path.join(input_dir, folder)
        pics = os.listdir(folder_path)
        pic_num += len(pics)
    
    print("There is %d persons." %folder_num)
    print("There is %d pictures of all person" %pic_num)
    print("finished all.")

    ### There is 25393 persons.
    ### There is 397640 pictures of all person

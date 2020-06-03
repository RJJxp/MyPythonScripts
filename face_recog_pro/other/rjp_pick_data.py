import os
import sys
import argparse
import shutil

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the input directory, `person_20200508` or `person_20200527`')
    parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def pickAndMove(input_dir, output_dir):
    # mkdir output dir if not exists
    # remove output dir if exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)

    # start to find the `a` folder
    # person_20200508/11/01/03/110103198311031573/a/*.jpg\
    # copy the `a` folder's pic to output dir
    # according to the id_card number
    # all the varialbe ended with `path` should be a directory
    count = 0
    id_12_folders = os.listdir(input_dir)
    for id_12_folder in id_12_folders:
        id_12_folder_path = os.path.join(input_dir, id_12_folder)
        id_34_folders = os.listdir(id_12_folder_path)
        for id_34_folder in id_34_folders:
            id_34_folder_path = os.path.join(id_12_folder_path, id_34_folder)
            id_56_folders = os.listdir(id_34_folder_path)
            for id_56_folder in id_56_folders:
                id_56_folder_path = os.path.join(id_34_folder_path, id_56_folder)
                id_folders = os.listdir(id_56_folder_path)
                for id_folder in id_folders:
                    id_foler_path = os.path.join(id_56_folder_path, id_folder)
                    abch_folders = os.listdir(id_foler_path)
                    for abch in abch_folders:
                        if abch == 'a':
                            print("%s" %id_folder)
                            # a_folder_path = os.path.join(id_foler_path, abch)
                            # dst_path = os.path.join(output_dir, id_folder)
                            # # copytree will automatic mkdir(dst)
                            # shutil.copytree(a_folder_path, dst_path)
                            # count += 1
                        else:
                            continue
                        
                        if (count % 100 == 0):
                            print("%d copyed." %count)

    print("finished pickAndMove func.")

if __name__ == "__main__":
    args= getArgs()
    input_dir = args.input_dir
    output_dir = args.output_dir
    pickAndMove(input_dir, output_dir)
    print("finished all.")
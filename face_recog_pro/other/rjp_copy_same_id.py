import os
import sys
import imageio
import argparse
import time
import random
import shutil

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record-path', type=str, help='Enter the record file path to write all the same record to the file.')
    parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def readRecord(record_path):
    fp = open(record_path, 'r')
    same_names = []
    idcard_paths = []
    photo_paths = []
    count = 0
    for record in fp:
        record = record.strip('\n')
        split_record = record.split(',')
        same_names.append(split_record[0])
        idcard_paths.append(split_record[1])
        photo_paths.append(split_record[2])
        count = count + 1
    for i in range(50):
        print(photo_paths[i])
    print('finished reading the record file.')
    return same_names, idcard_paths, photo_paths
    

# first copying the files to the destination
# IDcard image is named by the xxx_0001.jpg or xxx_0001.bmp
# the photo is name xxx_0002.jpg or xxx_002.bmp
def copy2OutputDir(output_dir, new_same_names, new_id_paths, new_photo_paths):
    # if the dir exists, delete it
    if os.path.exists(output_dir):
        # os.removedirs(output_dir)
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)
    # counters
    my_count = 0
    time1 = time.time()
    for name in new_same_names:
        # 2 src paths to copy from
        id_src_path = new_id_paths[new_same_names.index(name)]
        photo_src_path = new_photo_paths[new_same_names.index(name)]
        # start generate the 2 dst paths
        # folder path
        name_foler = os.path.join(output_dir, name)
        os.mkdir(name_foler)
        # id image dst path
        id_file_name = ''
        id_file_name += name
        id_file_name += '_0001'
        id_file_name += id_src_path[-4:]    # extension
        id_dst_path = os.path.join(name_foler, id_file_name)
        # photo image dst path
        photo_file_name = ''
        photo_file_name += name
        photo_file_name += '_0002'
        photo_file_name += photo_src_path[-4:]  # extension
        photo_dst_path = os.path.join(name_foler, photo_file_name)
        # copying
        shutil.copy(id_src_path, id_dst_path)
        shutil.copy(photo_src_path, photo_dst_path)
        time2 = time.time()
        my_count += 1
        print('the number %d, total time cost is %f' %(my_count, time2 - time1))
    print('finished copying')

if __name__ == '__main__':
    args = parseArgs()
    record_path = args.record_path
    output_dir = args.output_dir
    same_names, idcard_paths, photo_paths = readRecord(record_path)
    copy2OutputDir(output_dir, same_names, idcard_paths, photo_paths)
    print('finished all.')
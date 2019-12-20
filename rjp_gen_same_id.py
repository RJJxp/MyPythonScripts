import os
import sys
import imageio
import argparse
import time
import random
import shutil

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--idcard-dir', type=str, help='Enter the idcard directory.')
    parser.add_argument('--photos-dir', type=str, help='Enter the photos directory.')
    # parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    parser.add_argument('--record-path', type=str, help='Enter the record file path to write all the same record to the file.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

# in idcard_dir
# file name is the person's name
def getIDResult(idcard_dir):
    # value to return
    id_names = []
    id_paths = []
    child_dirs = os.listdir(idcard_dir)
    for child_dir in child_dirs: # 1, 2, 3, 6 folders 
        if (child_dir == '1' or child_dir == '2' or child_dir == '3' or child_dir == '6'):
            all_files = os.listdir(os.path.join(idcard_dir, child_dir))
            for id_pic in all_files:
                id_names.append(id_pic[0:-4])
                id_paths.append(os.path.join(idcard_dir, child_dir, id_pic))
        elif (child_dir == '4' or child_dir == '5'): # 4, 5 folders have one-step sub folders
            sub_child_dirs = os.listdir(os.path.join(idcard_dir, child_dir))
            for sub_child_dir in sub_child_dirs:
                all_files = os.listdir(os.path.join(idcard_dir, child_dir, sub_child_dir))
                for id_pic in all_files:
                    id_names.append(id_pic[0:-4])
                    id_paths.append(os.path.join(idcard_dir, child_dir, sub_child_dir, id_pic))
        elif (child_dir == 'handle_idcardImg.py'):  # ignore the file *.py
            continue
        else:   # should do nothing
            continue
    # test part
    print ('id_names len is %d' %len(id_names))
    print ('id_paths len is %d' %len(id_paths))
    # print (id_names[0])
    # print (id_names[-1])
    # print (id_paths[0])
    # print (id_paths[-1])
    return id_names, id_paths

# in the photos_dirs
# folder name is the person's name
# attetion: in each person's folder, there may be 2 or more photos of them
# one is RGB, the one is GRAY and others, we only need RGB
def getPhotoResult(photos_dir):
    # value to return
    photo_names = []
    photo_paths = []
    child_dirs = os.listdir(photos_dir)
    for child_dir in child_dirs:
        if (child_dir == '4'):  # 4 has one-step sub folders
            sub_child_dirs = os.listdir(os.path.join(photos_dir, child_dir))
            for sub_child_dir in sub_child_dirs:
                all_folders = os.listdir(os.path.join(photos_dir, child_dir, sub_child_dir))
                for folder in all_folders:
                    all_files = os.listdir(os.path.join(photos_dir, child_dir, sub_child_dir, folder))
                    for tfile in all_files:
                        if (tfile[-7:-4] == 'RGB'):  # only need the RGB pic
                            photo_names.append(folder)
                            this_photo_path = os.path.join(photos_dir, child_dir, sub_child_dir, folder, tfile)
                            photo_paths.append(this_photo_path)
                        elif(tfile[-6:-4] == 'IR'):
                            continue    # should do nothing
                        else:
                            continue    # should do nothing
                            # print(os.path.join(photos_dir, child_dir, sub_child_dir, folder, tfile))
        elif (child_dir == '1' or child_dir == '2' or child_dir == '3' or child_dir == '5' or child_dir == '6'):   
            all_folders = os.listdir(os.path.join(photos_dir, child_dir))
            for folder in all_folders:
                all_files = os.listdir(os.path.join(photos_dir, child_dir, folder))
                if (len(all_files) == 0):
                    print(os.path.join(photos_dir, child_dir, folder))
                for tfile in all_files:
                    if (tfile[-7:-4] == 'RGB'):
                        photo_names.append(folder)
                        this_photo_path = os.path.join(photos_dir, child_dir, folder, tfile)
                        photo_paths.append(this_photo_path)
                    elif (tfile[-6:-4] == 'IR'):
                        continue    # should do nothing
                    else:
                        continue    # should do nothing
                        # print(os.path.join(photos_dir, child_dir, folder, tfile))
        else:
            continue    # should do nothing
    print('photo_names len is %d' %len(photo_names))
    print('photo_paths len is %d' %len(photo_paths))
    return photo_names, photo_paths

# get rid of some id card pics that are too large
# which indicates it's not a ID card image
def findCommonIDandPhotos(id_names, id_paths, photo_names, photo_paths):
    # transfer from list to set
    id_names_set = set(id_names)
    photo_names_set = set(photo_names)
    my_count = 0
    # variable to return
    new_same_names = []
    new_id_paths = []
    new_photo_paths = []

    same_names_set = id_names_set.intersection(photo_names_set)
    print('there is %d same names' %len(same_names_set))
    same_names_list = list(same_names_set)
    random.shuffle(same_names_list)
    need_data_length = len(same_names_set)
    # need_data_length = 100
    same_names_list = same_names_list[0:need_data_length]
    time1 = time.time()
    for name in same_names_list:
        id_index = id_names.index(name)
        photo_index = photo_names.index(name)
        image = imageio.imread(id_paths[id_index])
        if (image.shape[0] < 200):
            new_same_names.append(name)
            new_id_paths.append(id_paths[id_index])
            new_photo_paths.append(photo_paths[photo_index])
        else:
            continue    # should do nothing
        # new_id_paths.append(id_paths[id_index])
        # new_photo_paths.append(photo_paths[photo_index])
        my_count += 1
        if my_count >= 1000:
            my_count = 0
            time2 = time.time()
            print('number %d, time %f' %(my_count, time2 - time1))
    
    print('%d %d %d' %(len(new_same_names), len(new_id_paths), len(new_photo_paths)))
    return new_same_names, new_id_paths, new_photo_paths

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

def writeSame2File(record_path, new_same_names, new_id_paths, new_photo_paths):
    fp = open(record_path, 'w')
    print('same name number is %d' %(len(new_same_names)))
    print('new id number is %d' %(len(new_id_paths)))
    print('new photo number is %d' %(len(new_photo_paths)))
    for i in range(len(new_same_names)):
        file_str = new_same_names[i] + ',' + new_id_paths[i] + ',' + new_photo_paths[i] + '\n'
        fp.writelines(file_str)
    fp.close()
    print('finished wirting all the record to the file.')


if __name__ == '__main__':
    # parse the args
    args = parseArgs()
    idcard_dir = args.idcard_dir
    photos_dir = args.photos_dir
    # output_dir = args.output_dir
    record_path = args.record_path
    # get people's idcard number and the path along with people's photo
    id_names, id_paths = getIDResult(idcard_dir)
    photo_names, photo_paths = getPhotoResult(photos_dir)
    # already know that id size is 73107, photo size is 52157
    if (len(id_names) == len(id_paths) and len(photo_names) == len(photo_paths)):
        print('pic and their path length is same')
    else:
        print('false')
        sys.exit(0)
    # get the intersection of id and photo names
    new_same_names, new_id_paths, new_photo_paths = findCommonIDandPhotos(id_names, id_paths, photo_names, photo_paths)
    # start copying the IDcard images and photos to the output-dir
    writeSame2File(record_path, new_same_names, new_id_paths, new_photo_paths)
    # copy2OutputDir(output_dir, new_same_names, new_id_paths, new_photo_paths)
    
    print ('finished all')

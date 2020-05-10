import os
import time
import shutil
import imageio
import argparse
from PIL import Image as PilImage

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the idcard directory.')
    parser.add_argument('--output-dir', type=str, help='Enter the idcard directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def bmp2jpg(input_dir, output_dir):
    # judge output_dir existence
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('outputdir already exists.')
    os.mkdir(output_dir)

    all_guys_folder = os.listdir(input_dir)
    precise_count = 0
    general_count = 0
    time1 = time.time()
    fp = open('/home/rjp/Desktop/error_record.txt', 'w')
    for guy_folder in all_guys_folder:
        precise_count += 1
        print_str = ''
        print_str += 'No.' + str(precise_count) + ' '
        # mkdir output
        guy_output_dir = os.path.join(output_dir, guy_folder)
        os.mkdir(guy_output_dir)
        # process input 
        guy_folder_dir = os.path.join(input_dir, guy_folder)
        guy_pics = os.listdir(guy_folder_dir)
        for guy_pic in guy_pics:
            try:    # some pic can not open, there will be IOError
                # input path
                guy_input_path = os.path.join(input_dir, guy_folder, guy_pic)
                if (guy_pic[-4:] == '.bmp'):    # should open the pic and save it as .jpg
                    guy_output_path = os.path.join(guy_output_dir, guy_pic[:-4] + '.jpg')
                    PilImage.open(guy_input_path).save(guy_output_path)
                elif (guy_pic[-4:] == '.jpg'):  # simply copy 
                    guy_output_path = os.path.join(guy_output_dir, guy_pic)
                    shutil.copy(guy_input_path, guy_output_path)
                else:   # should do nothing
                    continue
            except IOError:
                fp.writelines(guy_pic + '\n')
                print('There is an Error, write down it')
            else:    
                continue
        time2 = time.time()
        if precise_count >= 1000:
            general_count += 1
            precise_count = 0
            print('No %d used time %f' %(general_count * 1000, time2 - time1))
    fp.close()

if __name__ == '__main__':
    args = getArgs()
    input_dir = args.input_dir
    output_dir = args.output_dir
    print('finished arg parsing and start bmp2jpg.')
    bmp2jpg(input_dir, output_dir)
    print('finished all.')

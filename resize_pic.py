import argparse
import io
import os
import shutil
from PIL import Image as PilImage 

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the origin directory.')
    parser.add_argument('--output-dir', type=str, help='Enter the output directory.')
    parser.add_argument('--width', type=int, default=720, help='Enter the resized width')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def resizeIt(in_dir, out_dir, resize_w):
    print("start resizing.")
    # judge output_dir existence
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
        print('outputdir already exists.')
    os.mkdir(out_dir)
    
    for pic_name in os.listdir(in_dir):
        pic_path = os.path.join(in_dir, pic_name)
        pic = PilImage.open(pic_path)
        pic_w, pic_h = pic.size
        resize_h = resize_w / pic_w * pic_h
        pic_resize = pic.resize((resize_w, int(resize_h)))
        save_path = os.path.join(out_dir, pic_name)
        pic_resize.save(save_path)
        print("resized %s" %pic_name)

    print("finished all pics in in_dir resizing.")

if __name__ == "__main__":
    args = getArgs()
    in_dir = args.input_dir
    out_dir = args.output_dir
    resized_w = args.width
    resizeIt(in_dir, out_dir, resized_w)

    print("finished all.")
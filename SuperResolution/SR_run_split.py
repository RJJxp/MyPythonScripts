import io
import os
import sys
import argparse
from SR_class import *

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the directory of the input')
    parser.add_argument('--output-dir', type=str, help='Enter the directory of the output')
    parser.add_argument('--sample-step', type=int, help='Enter sample step')
    parser.add_argument('--sample-size', type=int, help='Enter sample size')

    args = parser.parse_args()
    print ("parse args complete")
    return args

if __name__ == "__main__":
    args = getArgs()
    input_dir = args.input_dir
    output_dir = args.output_dir
    s_step = args.sample_step
    s_size = args.sample_size
    img_split = ImgSplit()
    img_split.setPara(s_step, s_size)
    img_split.splitImgDir(input_dir, output_dir)
    print("Finished main.")
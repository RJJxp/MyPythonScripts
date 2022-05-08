import os
from SR_class import *

input_dir = r"D:\MyPictures\20211127avatar"

if __name__ == "__main__":
    calRGBmean = ImgMeanStd()
    calRGBmean.calRGB_mean(input_dir)

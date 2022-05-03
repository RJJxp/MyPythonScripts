import os
from SR_class import *

S2_TIFF_DIR = r"G:\SR_DATASET_RJP\20200129_SUBSET\TIFF_S2"
S2_PNG_DIR = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_TEST_S2"

GF_TIFF_DIR = r"G:\SR_DATASET_RJP\20200129_SUBSET\TIFF_GF"
GF_PNG_DIR = r"G:\SR_DATASET_RJP\20200129_SUBSET\PNG_TEST_GF"

if __name__ == "__main__":
    img_resize = ImgResize()
    img_resize.subsetImg(S2_TIFF_DIR, S2_PNG_DIR)
    img_resize.subsetImg(GF_TIFF_DIR, GF_PNG_DIR)
    print("Finished script SR_Shell_part00.")
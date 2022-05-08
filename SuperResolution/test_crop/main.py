import os 
import argparse
from SRdataset import *

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-pdir', type=str, help='Enter the input parent dir of S2 and GF tiff data.')
    parser.add_argument('--split', action="store_true", help='(subset and split) or not. Used in first step.')
    parser.add_argument('--intersect', action="store_true", help='intersect of GF and S2 data. Used in second step.')
    parser.add_argument('--match', action="store_true", help='match or not. Used in third step.')
    parser.add_argument('--rename', action="store_true", help='rename or not. Used in fourth(last) step.')
    parser.add_argument('--datachoice', type=str, choices=["gf2s2", "gf1s2"], help='gf2s2 or gf1s2')
    
    args = parser.parse_args()
    print ("parse args complete")
    return args

def generateAllDirs(input_pdir):
    dirs_dict = {"pdir":input_pdir}
    tiff_dir = os.path.join(input_pdir, "TIFF_")
    png_dir = os.path.join(input_pdir, "PNG_")
    split_dir = os.path.join(input_pdir, "SPLIT_")
    common_dir = os.path.join(input_pdir, "COMMON_")
    match_dir = os.path.join(input_pdir, "MATCH_")
    rename_dir = os.path.join(input_pdir, "RENAME_")

    dirs_dict["tiff_dir"] = tiff_dir
    dirs_dict["png_dir"] = png_dir
    dirs_dict["split_dir"] = split_dir
    dirs_dict["common_dir"] = common_dir
    dirs_dict["match_dir"] = match_dir
    dirs_dict["rename_dir"] = rename_dir

    print("generate all dirs.")
    return dirs_dict

def generateSplitParam(data_choice):
    split_param = {"name": data_choice}
    if data_choice == "gf2s2":  # gf2 and s2, 10:1
        split_param["s2step"] = 100
        split_param["s2size"] = 100
        split_param["gfstep"] = 1000
        split_param["gfsize"] = 1000

    else:   # gf1 and s2, 5:1
        split_param["s2step"] = 100
        split_param["s2size"] = 100
        split_param["gfstep"] = 500
        split_param["gfsize"] = 500
    
    print("finished generating split parameters...")
    return split_param

def resizeIMG(all_dirs):
    s2_tiff_dir = all_dirs["tiff_dir"] + "S2"
    s2_png_dir = all_dirs["png_dir"] + "S2"
    gf_tiff_dir = all_dirs["tiff_dir"] + "GF"
    gf_png_dir = all_dirs["png_dir"] + "GF"

    img_resize = ImgResize()
    img_resize.subsetImg(s2_tiff_dir, s2_png_dir)
    img_resize.subsetImg(gf_tiff_dir, gf_png_dir)
    print("finished resize...")

def splitIMG(all_dirs, split_param):
    s2_step = split_param["s2step"]
    s2_size = split_param["s2size"]
    gf_step = split_param["gfstep"]
    gf_size = split_param["gfsize"]
    s2_png_dir = all_dirs["png_dir"] + "S2"
    s2_split_dir = all_dirs["split_dir"] + "S2"
    gf_png_dir = all_dirs["png_dir"] + "GF"
    gf_split_dir = all_dirs["split_dir"] + "GF"

    img_split = ImgSplit()
    # split s2 img
    img_split.setPara(s2_step, s2_size)
    img_split.splitImgDir(s2_png_dir, s2_split_dir)
    print("====== finshed s2 split ======")
    # split gf img
    img_split.setPara(gf_step, gf_size)
    img_split.splitImgDir(gf_png_dir, gf_split_dir)
    print("====== finshed gf split ======")

    print("finished splitIMG function...")

def intersectIMG(all_dirs):
    s2_split_good_dir = all_dirs["split_dir"] + "S2good"
    s2_common_dir = all_dirs["common_dir"] + "S2"
    gf_split_dir = all_dirs["split_dir"] + "GF"
    gf_common_dir = all_dirs["common_dir"] + "GF"
    
    img_check = ImgCheck()
    img_check.getIntersection(gf_split_dir, s2_split_good_dir, gf_common_dir, s2_common_dir)

    # s2_match_good_dir = all_dirs["match_dir"] + "S2good"
    # s2_commonv2_dir = all_dirs["common_dir"] + "S2v2"
    # gf_common_dir = all_dirs["common_dir"] + "GF"
    # gf_commonv2_dir = all_dirs["common_dir"] + "GFv2"
    
    # img_check = ImgCheck()
    # img_check.getIntersection(gf_common_dir, s2_match_good_dir, gf_commonv2_dir, s2_commonv2_dir)

    print("finished intersectFunc ....")

def matchIMG(all_dirs):
    s2_common_dir = all_dirs["common_dir"] + "S2"
    s2_match_dir = all_dirs["match_dir"] + "S2"
    gf_common_dir = all_dirs["common_dir"] + "GF"
    # gf_match_dir = all_dirs["match_dir"] + "GF"
    img_match = ImgMatch()
    img_match.runIt(s2_common_dir, gf_common_dir, s2_match_dir)
    print("finished matchIMG function...")

def renameIMG(all_dirs):
    s2_match_dir = all_dirs["match_dir"] + "S2"
    s2_rename_dir = all_dirs["rename_dir"] + "S2"
    gf_common_dir = all_dirs["common_dir"] + "GF"
    gf_rename_dir = all_dirs["rename_dir"] + "GF"
    img_rename = ImgRename()
    img_rename.renameByIdx(s2_match_dir, s2_rename_dir)
    img_rename.renameByIdx(gf_common_dir, gf_rename_dir)
    print("finished func renameIMG()...")

if __name__ == "__main__":
    args = getArgs()
    
    all_dirs = generateAllDirs(args.input_pdir)
    split_param = generateSplitParam(args.datachoice)

    # resizing the img of gf takes long time
    # so there is a flag to control to resize 
    if args.split:
        # resizeIMG(all_dirs)
        # split img to pieces
        splitIMG(all_dirs, split_param)

    if args.intersect:
        intersectIMG(all_dirs)

    if args.match:
        matchIMG(all_dirs)
    
    if args.rename:
        renameIMG(all_dirs)
    
    print("finished main.")
import io
import os
import sys
import numpy as np
import shutil
import cv2 as cv
from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
from color_matcher.normalizer import Normalizer
import numpy as np

#######################
### Class ImgResize ###
#######################
#  Remeber to modify `width` and `height`
class ImgResize:
    width = 1000
    height = 1000

    def __init__(self) -> None:
        pass
    
    def setHeightWidth(self, height_s, width_s):
        self.height = height_s
        self.width = width_s

    def resizeImg(self, input_dir, output_dir):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print('outdir already exists.')
        os.mkdir(output_dir)

        for img_name in os.listdir(input_dir):
            img_path = os.path.join(input_dir, img_name)
            img = cv.imread(img_path)
            dim = (self.height, self.width)
            resized_img = cv.resize(img, dim, interpolation=cv.INTER_LINEAR)

            output_path = os.path.join(output_dir, img_name)
            cv.imwrite(output_path, resized_img)
            print("Finished %s resized" %img_name)
        print("Finished all img resized.")
    
    # use to make 8001*8001.tiff to 8000*8000.png
    def subsetImg(self, input_dir, output_dir):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print('outdir already exists.')
        os.mkdir(output_dir)

        img_names = os.listdir(input_dir)
        for img in img_names:
            img_path = os.path.join(input_dir, img)
            img = cv.imread(img_path, 1)
            height = np.shape(img)[0]
            width = np.shape(img)[1]
            img_out = img[0:height-1, 0:width-1]
            img_name = os.path.basename(img_path)[:-4]
            output_path = os.path.join(output_dir, img_name+".png")
            cv.imwrite(output_path, img_out)
        print("Finished subset Img.")

    def tiff2PNG(self, input_dir, output_dir):
        tiff_names = os.listdir(input_dir)
        for img in tiff_names:
            img_path = os.path.join(input_dir, img)
            img = cv.imread(img_path, 1)
            img_name = os.path.basename(img_path)[:-4]
            output_path = os.path.join(output_dir, img_name+".png")
            cv.imwrite(output_path, img)
        print("Finished TIFF to PNG")


######################
### Class ImgSplit ###
######################
class ImgSplit:
    __sample_step = 0
    __sample_size = 0

    def __init__(self) -> None:
        pass

    def __sampleCount(self, length):
        count = (length - self.__sample_size) * 1.0 / self.__sample_step
        count = int(count) + 1
        return count

    def setPara(self, s_step, s_size):
        self.__sample_step = s_step
        self.__sample_size = s_size
        print("step: %d" %self.__sample_step)
        print("size: %d" %self.__sample_size)
    
    def splitImg(self, img_path, output_dir):
        img_name = os.path.basename(img_path)[:-4]
        img = cv.imread(img_path)
        height = np.shape(img)[0]
        width = np.shape(img)[1]
        h_count = self.__sampleCount(height)
        w_count = self.__sampleCount(width)
        print("h:%d, w:%d" %(h_count, w_count))
        for h_c in range(h_count):
            for w_c in range(w_count):
                h = h_c * self.__sample_step
                w = w_c * self.__sample_step
                sub_img = img[h:h + self.__sample_size, w:w + self.__sample_size,:]
                output_path = os.path.join(output_dir, img_name + "_%02d%02d" %(h_c, w_c) + ".png")
                cv.imwrite(output_path, sub_img)
                # print("finished _%02d%02d" %(h_c, w_c))
        print("Finished %s split." %img_name)
    
    def splitImgDir(self, input_dir, output_dir):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print('outdir already exists.')
        os.mkdir(output_dir)

        for img_name in os.listdir(input_dir):
            img_path = os.path.join(input_dir, img_name)
            self.splitImg(img_path, output_dir)

###########################
### Class ImgColorMatch ###
###########################
class ImgMatch:
    def __init__(self) -> None:
        pass
    
    def runIt(self, src_dir, ref_dir, out_dir):
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
            print('outdir already exists.')
        os.mkdir(out_dir)

        for srcname, refname in zip(os.listdir(src_dir), os.listdir(ref_dir)):
            srcimg_path = os.path.join(src_dir, srcname)
            refimg_path = os.path.join(ref_dir, refname)
            img_src = load_img_file(srcimg_path)
            img_ref = load_img_file(refimg_path)
            obj = ColorMatcher(src=img_src, ref=img_ref, method="hm")
            img_res = obj.main()
            img_res = Normalizer(img_res).uint8_norm()
            out_path = os.path.join(out_dir, srcname)
            save_img_file(img_res, out_path)
            print("finished %s" %(out_path))

#######################
### Class ImgRename ###
#######################
class ImgRename:
    # rename according to DIV2K
    def __init__(self) -> None:
        pass

    def renameLR(self, indir, outdir, scale):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
            print('outdir already exists.')
        os.mkdir(outdir)

        img_names = os.listdir(indir)
        for img_name in img_names:
            inpath = os.path.join(indir, img_name)
            outpath = os.path.join(outdir, img_name[:-4] + "x%d.png" %scale)
            shutil.copy(inpath, outpath)
        print("Finished copy and rename LR dataset")

    def renameHR(self, indir, outdir):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
            print('outdir already exists.')
        os.mkdir(outdir)

        img_names = os.listdir(indir)
        for img_name in img_names:
            inpath = os.path.join(indir, img_name)
            outpath = os.path.join(outdir, img_name[:-4] + ".png")
            shutil.copy(inpath, outpath)
        print("Finished copy and rename HR dataset")

    def renameByIdx(self, indir, outdir):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
            print('outdir already exists.')
        os.mkdir(outdir)

        img_names = os.listdir(indir)
        img_num = len(img_names)
        for idx in range(img_num):
            inpath = os.path.join(indir, img_names[idx])
            outname = "%04d.png" %(idx+1)
            outpath = os.path.join(outdir, outname)
            shutil.copy(inpath, outpath)
        print("finished copy and rename data by index.")


################
### ImgCheck ###
################
class ImgCheck:

    def __init__(self) -> None:
        pass

    def getIntersection(self, dir01, dir02, outdir01, outdir02):
        if os.path.exists(outdir01):
            shutil.rmtree(outdir01)
            print('outputdir01 already exists.')
        os.mkdir(outdir01)

        if os.path.exists(outdir02):
            shutil.rmtree(outdir02)
            print('outputdir01 already exists.')
        os.mkdir(outdir02)

        img_names_01 = os.listdir(dir01)
        idx_01 = []
        for img_name_01 in img_names_01:
            idx_01.append(img_name_01[0:4] + img_name_01[-8:-4])
        print(len(idx_01))

        img_names_02 = os.listdir(dir02)
        idx_02 = []
        for img_name_02 in img_names_02:
            idx_02.append(img_name_02[0:4] + img_name_02[-8:-4])
        print(len(idx_02))

        common_idx_set = set.intersection(set(idx_01), set(idx_02))
        print(len(common_idx_set))
        common_idx = list(common_idx_set)
        for idx in common_idx:
            # gf part
            gf_filename = idx[0:4] + "GF_" + idx[4:8] + ".png"
            inpath01 = os.path.join(dir01, gf_filename)
            outpath01 = os.path.join(outdir01, gf_filename)
            shutil.copy(inpath01, outpath01)
            # s2 part
            s2_filename = idx[0:4] + "S2_" + idx[4:8] + ".png"
            # s2_filename = idx[0:7] + "_S2_" + idx[7:11] + ".png"
            inpath02 = os.path.join(dir02, s2_filename)
            outpath02 = os.path.join(outdir02, s2_filename)
            shutil.copy(inpath02, outpath02)

            # print("copy %s done" %idx)

    def check2Folder(self, dir01, dir02):
        imgs01 = os.listdir(dir01)
        imgs02 = os.listdir(dir02)
        for img01, img02 in zip(imgs01, imgs02):
            if img01[:-4] != img02[:-4]:
                print("%s not match %s" %(img01, img02))
                return False
            else:
                pass
        return True 
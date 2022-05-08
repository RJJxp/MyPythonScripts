import io
import os
import sys
import numpy as np
import shutil
import cv2 as cv
from skimage import metrics
from skimage import io


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


# need to setup the `keywords` in function `mvMatchedImg`
class ImgMatch:
    def __init__(self) -> None:
        pass

    def __genSingleCommand(self, base_img_path, warp_img_path):
        color_match_command = "color-matcher -s %s -r %s" %(warp_img_path, base_img_path)
        return color_match_command

    def genAllCommand(self, base_img_dir, warp_img_dir):
        cm_commands = []
        base_img_names = os.listdir(base_img_dir)
        warp_img_names = os.listdir(warp_img_dir)
        base_img_names = sorted(base_img_names)
        warp_img_names = sorted(warp_img_names)
        for base_img_name, warp_img_name in zip(base_img_names, warp_img_names):
            base_flag = base_img_name[0:7] + base_img_name[-8:-4]
            warp_flag = warp_img_name[0:7] + warp_img_name[-8:-4]
            if base_flag != warp_flag:
                print("%s not match %s" %(base_img_name[:-4], warp_img_name[:-4]))
                continue 
            base_img_path = os.path.join(base_img_dir, base_img_name)
            warp_img_path = os.path.join(warp_img_dir, warp_img_name)
            str = self.__genSingleCommand(base_img_path, warp_img_path)
            cm_commands.append(str)
        print("%d command totally." % len(cm_commands))
        return cm_commands
    
    def mvMatchedImg(self, input_warp_dir, output_warp_dir):
        if os.path.exists(output_warp_dir):
            shutil.rmtree(output_warp_dir)
            print('outdir already exists.')
        os.mkdir(output_warp_dir)

        keywords = ["default"]
        warp_img_names = os.listdir(input_warp_dir)
        for i in range(len(warp_img_names)):
            for kword in keywords:
                if kword in warp_img_names[i]:
                    input_path = os.path.join(input_warp_dir, warp_img_names[i])
                    output_path = os.path.join(output_warp_dir, warp_img_names[i])
                    shutil.move(input_path, output_path)
                    # print("No.%04d moved" %i)
                else:
                    pass

        # for warp_img_name in os.listdir(input_warp_dir):
        #     for kword in keywords:
        #         if kword in warp_img_name:
        #             input_path = os.path.join(input_warp_dir, warp_img_name)
        #             output_path = os.path.join(output_warp_dir, warp_img_name)
        #             shutil.move(input_path, output_path)
        #         else:
        #             continue
        print("Finished move matched img.")

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
            idx_01.append(img_name_01[0:7] + img_name_01[11:15])
        print(len(idx_01))

        img_names_02 = os.listdir(dir02)
        idx_02 = []
        for img_name_02 in img_names_02:
            idx_02.append(img_name_02[0:7] + img_name_02[11:15])
        print(len(idx_02))

        common_idx_set = set.intersection(set(idx_01), set(idx_02))
        print(len(common_idx_set))
        common_idx = list(common_idx_set)
        for idx in common_idx:
            # gf part
            gf_filename = idx[0:7] + "_GF_" + idx[7:11] + ".png"
            inpath01 = os.path.join(dir01, gf_filename)
            outpath01 = os.path.join(outdir01, idx + ".png")
            shutil.copy(inpath01, outpath01)
            # s2 part
            s2_filename = idx[0:7] + "_S2_" + idx[7:11] + "_default.png"
            # s2_filename = idx[0:7] + "_S2_" + idx[7:11] + ".png"
            inpath02 = os.path.join(dir02, s2_filename)
            outpath02 = os.path.join(outdir02, idx + ".png")
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
            out_name = img_name[0:7] + img_name[-8:-4] + "x%d.png" %scale
            outpath = os.path.join(outdir, out_name)
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
            out_name = img_name[0:7] + img_name[11:15] + ".png"
            outpath = os.path.join(outdir, out_name)
            shutil.copy(inpath, outpath)
        print("Finished copy and rename HR dataset")

class ImgMeanStd:
    # cal rgb_mean 
    def __init__(self) -> None:
        pass

    # for png
    def calRGB_mean(self, input_dir):
        r_total = 0.0
        g_total = 0.0
        b_total = 0.0
        N_total = 0
        rgb_range = 255
        img_names = os.listdir(input_dir)
        img_number = len(img_names)
        for img_name in img_names:
            img_path = os.path.join(input_dir, img_name)
            img = cv.imread(img_path)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = np.array(img)
            h, w, c = img.shape
            N_total += h * w
            r = img[:, :, 0]
            r_total += np.sum(r)
            g = img[:, :, 1]
            g_total += np.sum(g)
            b = img[:, :, 2]
            b_total += np.sum(b)

        print("There is %d img" %img_number)
        print("rgb total: %f %f %f" %(r_total, g_total, b_total))
        print("total pixel number: %d" %(N_total))
        r_mean = r_total / N_total
        g_mean = g_total / N_total
        b_mean = b_total / N_total
        print("rgb_mean is: ")
        print("r_mean: %f" %r_mean)
        print("g_mean: %f" %g_mean)
        print("b_mean: %f" %b_mean)
        print("rgb_mean by range: ")
        print("r_mean: %f" %(r_mean / rgb_range))
        print("g_mean: %f" %(g_mean / rgb_range))
        print("b_mean: %f" %(b_mean / rgb_range))

class ImgMetrics:
    def __init__(self) -> None:
        pass
    
    def cal_psnr_ssim(self, img_path01, img_path02):
        img01 = io.imread(img_path01)
        img02 = io.imread(img_path02)
        ssim_value = metrics.structural_similarity(img01, img02, data_range=255, channel_axis=2)
        psnr_value = metrics.peak_signal_noise_ratio(img01, img02, data_range=255)
        return psnr_value, ssim_value

    def cal_psnr_ssim_folder(self, sr_dir, gt_dir):
        sr_img_names = os.listdir(sr_dir)
        gt_img_names = os.listdir(gt_dir)
        assert len(sr_img_names) == len(gt_img_names)
        sr_img_names = sorted(sr_img_names)
        gt_img_names = sorted(gt_img_names)
        psnr_list = []
        ssim_list = []
        for sr_img_name, gt_img_name in zip(sr_img_names, gt_img_names):
            print("%s %s" %(sr_img_name, gt_img_name))
            sr_img_path = os.path.join(sr_dir, sr_img_name)
            gt_img_path = os.path.join(gt_dir, gt_img_name)
            psnr, ssim = self.cal_psnr_ssim(sr_img_path, gt_img_path)
            psnr_list.append(psnr)
            ssim_list.append(ssim)
            print("psnr: %f" %psnr)
            print("ssim: %f" %ssim)
        average_psnr = sum(psnr_list) / len(sr_img_names)
        average_ssim = sum(ssim_list) / len(sr_img_names)
        print("average pnsr: %f" %average_psnr)
        print("average ssim: %f" %average_ssim)

        

        






        


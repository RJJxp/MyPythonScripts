from SR_class import *
import os


if __name__ == "__main__":
    sr_dir = r"D:\work\realESRGAN_results\GANrealMfakeD"
    gt_dir = r"D:\work\TestDataset\0504faketest\HR"
    img_metrics = ImgMetrics()
    img_metrics.cal_psnr_ssim_folder(sr_dir, gt_dir)
    print("finished all.")
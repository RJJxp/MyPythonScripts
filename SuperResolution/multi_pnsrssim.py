from skimage import metrics
from skimage import io
import os

# conda activate pix2pix
# for metaSR test
# if __name__ == "__main__":
#     input_dir = r"G:\RJP_metaSR\Meta-SR-Pytorch\experiment\metarjprdn\results"

#     for i in list(range(63)):
#         hr_img_name = "%04d_x5.0_HR.png" %(i+1)
#         sr_img_name = "%04d_x5.0_SR.png" %(i+1)
#         hr_img_path = os.path.join(input_dir, hr_img_name)
#         sr_img_path = os.path.join(input_dir, sr_img_name)
#         hr_img = io.imread(hr_img_path)
#         sr_img = io.imread(sr_img_path)

#         ssim_value = metrics.structural_similarity(hr_img, sr_img, data_range=255, multichannel=True)
#         pnsr_value = metrics.peak_signal_noise_ratio(hr_img, sr_img, data_range=255)
#         print("========== No.%04d ==========" %(i+1))
#         print("ssim: %s" %ssim_value)
#         print("pnsr: %s" %pnsr_value)

# # conda activate pix2pix
# # pix2pix ssim pnsr for realB and fakeB
# if __name__ == "__main__":
#     input_dir = r"D:\RJP_stuff\20211227\results_pix2pix\test_200\images"

#     img_names = os.listdir(input_dir)
#     fake_B_idx = []
#     for i in range(len(img_names)):
#         if "fake_B" in img_names[i]:
#             fake_B_idx.append(i)
    
#     for fake_i in fake_B_idx:
#         fake_B_img_name = img_names[fake_i]
#         real_B_img_name = img_names[fake_i + 2]
#         fake_B_img_path = os.path.join(input_dir, fake_B_img_name)
#         real_B_img_path = os.path.join(input_dir, real_B_img_name)
#         fake_B_img = io.imread(fake_B_img_path)
#         real_B_img = io.imread(real_B_img_path)
        
#         ssim_value = metrics.structural_similarity(fake_B_img, real_B_img, data_range=255, multichannel=True)
#         pnsr_value = metrics.peak_signal_noise_ratio(fake_B_img, real_B_img, data_range=255)
#         print("===== %s =====" %fake_B_img_name)
#         print("ssim: %s" %ssim_value)
#         print("pnsr: %s" %pnsr_value)


from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
from color_matcher.normalizer import Normalizer
import numpy as np

# # conda activate SR_dataset
# # get pix2pix histogram match result
# if __name__ == "__main__":
#     input_dir = r"D:\RJP_stuff\20211227\results_pix2pix\test_200\images"
#     output_dir = r"D:\RJP_stuff\20211227\results_pix2pix\test_colormatch"
#     img_names = os.listdir(input_dir)
#     fake_B_idx = []
#     for i in range(len(img_names)):
#         if "fake_B.png" in img_names[i]:
#             fake_B_idx.append(i)
    
#     for fake_i in fake_B_idx:
#         fake_B_img_name = img_names[fake_i]
#         real_B_img_name = img_names[fake_i + 2]
#         fake_B_img_path = os.path.join(input_dir, fake_B_img_name)
#         real_B_img_path = os.path.join(input_dir, real_B_img_name)
#         fake_B_img = io.imread(fake_B_img_path)
#         real_B_img = io.imread(real_B_img_path)

#         img_ref = load_img_file(real_B_img_path)
#         img_src = load_img_file(fake_B_img_path)
#         obj = ColorMatcher(src=img_src, ref=img_ref, method='mvgd')
#         img_res = obj.main()
#         img_res = Normalizer(img_res).uint8_norm()
#         fake_B_cm_name = fake_B_img_name[:-4] + "_mvgd" + ".png"
#         fake_B_cm_path = os.path.join(output_dir, fake_B_cm_name)
#         save_img_file(img_res, fake_B_cm_path)
#         print("finished %s" %(fake_B_img_name))


# after get the color match result
# see the ssim and pnsr 
if __name__ == "__main__":
    real_img_dir = r"D:\RJP_stuff\20211227\results_pix2pix\test_200\images"
    match_img_dir = r"D:\RJP_stuff\20211227\results_pix2pix\test_colormatch"
    # methods_list = ["hm", "reinhard", "mvgd", "mkl"]

    real_img_names = os.listdir(real_img_dir)
    real_B_idx = []
    for i in range(len(real_img_names)):
        if "real_B.png" in real_img_names[i]:
            real_B_idx.append(i)

    for real_i in real_B_idx:
        real_img_name = real_img_names[real_i]
        real_img_path = os.path.join(real_img_dir, real_img_name)
        real_img = io.imread(real_img_path)

        fake_img_name = real_img_names[real_i - 2]
        fake_img_path = os.path.join(real_img_dir, fake_img_name)
        fake_img = io.imread(fake_img_path)

        fake_ssim_value = metrics.structural_similarity(real_img, fake_img, data_range=255, multichannel=True)
        fake_pnsr_value = metrics.peak_signal_noise_ratio(real_img, fake_img, data_range=255)
        # print("===== %s =====" %fake_img_name)
        # print("fake_ssim: %s" %fake_ssim_value)
        # print("fake_pnsr: %s" %fake_pnsr_value)

        real_img_id = real_img_name[:-10]
        for match_name in os.listdir(match_img_dir):
            if (real_img_id in match_name) and ("hm" in match_name) :
                match_img_path = os.path.join(match_img_dir, match_name)
                match_img = io.imread(match_img_path)
                match_ssim_value = metrics.structural_similarity(real_img, match_img, data_range=255, multichannel=True)
                match_pnsr_value = metrics.peak_signal_noise_ratio(real_img, match_img, data_range=255)
                # print("===== %s =====" %match_name)
                # print("ssim: %s" %match_ssim_value)
                # print("pnsr: %s" %match_pnsr_value)

                if (fake_ssim_value < match_ssim_value) and (fake_pnsr_value < match_pnsr_value):
                    print("%s" %real_img_name)
                    print("ssim: %s \t %s" %(fake_ssim_value, match_ssim_value))
                    print("pnsr: %s \t %s" %(fake_pnsr_value, match_pnsr_value))

        



    

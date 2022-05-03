import os
from SR_class import *

# resize part
input_dir_resize = r"/home/xuwh/Documents/20220427_dataset/PNG_GF"
output_dir_resize = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized"
resized_width = 6400
resized_height = 6400

# gf split
input_dir_gf = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized"
output_dir_gf = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized_split"
sample_step_gf = 1600
sample_size_gf = 1600

# s2 split
input_dir_s2 = r"/home/xuwh/Documents/20220427_dataset/PNG_S2"
output_dir_s2 = r"/home/xuwh/Documents/20220427_dataset/PNG_S2_split"
sample_step_s2 = 400
sample_size_s2 = 400

# histogram match
input_base_dir = r"/home/xuwh/Documents/20220427_dataset/PNG_S2_split"
input_warp_dir = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized_split"
output_warp_dir = r"/home/xuwh/Documents/20220427_dataset/PNG_GF_resized_split_match"

if __name__ == "__main__":
    # resize 
    img_resize = ImgResize()
    img_resize.setHeightWidth(resized_height, resized_width)
    img_resize.resizeImg(input_dir_resize, output_dir_resize)
    print("=====================\nFinished Resize Part\n=====================\n\n")

    # gf split 
    command_str = "python SR_run_split.py --input-dir %s --output-dir %s --sample-step %d --sample-size %d" \
                  %(input_dir_gf, output_dir_gf, sample_step_gf, sample_size_gf)
    os.system(command_str)
    print("=====================\nFinished GF Split Part\n=====================\n\n")

    # s2 split 
    command_str = "python SR_run_split.py --input-dir %s --output-dir %s --sample-step %d --sample-size %d" \
                  %(input_dir_s2, output_dir_s2, sample_step_s2, sample_size_s2)
    os.system(command_str)
    print("=====================\nFinished S2 Split Part\n=====================\n\n")

    # histogram match 
    img_match = ImgMatch()
    all_commands = img_match.genAllCommand(input_base_dir, input_warp_dir)
    for cm_command in all_commands:
        os.system(cm_command)
    img_match.mvMatchedImg(input_warp_dir, output_warp_dir)
    print("=====================\nFinished Histogram Match Part\n=====================\n\n")

    print("Finished shell main.")
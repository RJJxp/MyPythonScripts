from scipy import io as sciio
import numpy as np
import cv2

label_mat_data = sciio.loadmat("test02.mat")
print(label_mat_data.keys())

label_data = label_mat_data["out_data"]

print("Class: %s" %np.max(label_data))
label2color_dict = {
        0: [0, 0, 0],
        1: [255, 0, 0],  # red
        2: [0, 255, 0],  # green
        3: [0, 0, 255],  # blue
        4: [0, 255, 255],  # peru
        5: [255, 0, 255],  # purple
        6: [255, 255, 0],  # brown1
        7: [139, 69, 19],  # Chocolate4
    }

print(np.shape(label_data))

visual_anno = np.zeros((label_data.shape[0], label_data.shape[1], 3), dtype=np.uint8)
for i in range(visual_anno.shape[0]):  # i for h
    for j in range(visual_anno.shape[1]):
        color = label2color_dict[label_data[i, j]]
        visual_anno[i, j, 0] = color[2]
        visual_anno[i, j, 1] = color[1]
        visual_anno[i, j, 2] = color[0]

cv2.imwrite("test02.png", visual_anno)


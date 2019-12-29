import os
import itertools
import time
from PIL import Image as PilImage
import imageio
# s = "rjp_0001.jpg"
# folder_1 = "/home/rjp/Documents"
# folder_2 = "/home/rjp/Documents/test1"
# folder_3 = "/home/rjp/Documents/test1/test2"

# s = "rjp_0001.jpg"
# folder_1 = "/home/rjp/Documents"
# folder_2 = "/home/rjp/Documents/test1"
# folder_3 = "/home/rjp/Documents/test1/test2"

# ss = s3[-3:-1]
# print(ss)
try:
    PilImage.open('/home/rjp/Desktop/420281199411046539_0002.bmp')
except IOError:
    print('There is an Error')
else:
    print('no problem')
# imageio.imread('/home/rjp/Desktop/420281199411046539_0002.bmp')
# os.mkdir(folder_2)
# os.mkdir(folder_3)

# os.makedirs(folder_3)

# combs = list(itertools.combinations(range(4), 2))
# for comb in combs:
#     print(comb[0])
#     print(comb[1])

for i in range(3, 5):
    print(i)
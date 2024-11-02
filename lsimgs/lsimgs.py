import os
import argparse

import cv2
import numpy as np

def is_image(file, types):
    res = False
    for t in types:
        if file.endswith("." + t):
            res = True
            break
    return res

def get_output(folder, types):
    img_names = [fn for fn in os.listdir(folder) if is_image(fn, types)]

    res_list = []
    for img_name in img_names:
        img = cv2.imread(os.path.join(folder, img_name), cv2.IMREAD_UNCHANGED)
        res_list.append({"image": img_name, "shape": img.shape, "dtype": img.dtype, "min": np.min(img), "max": np.max(img)})
    return res_list

def dict2str(d):
    res = ""
    for key in d:
        res += "{0}: {1}; ".format(key, d[key])
    return res

if __name__ == "__main__":
    all_types = [
        "bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp",
        "pbm", "pgm", "ppm", "pxm", "pnm", "sr", "ras", "tiff",
        "tif", "exr", "hdr", "pic"
    ]
    parser = argparse.ArgumentParser(prog = "lsimgs",
                                     description = "A program that displays data about images in a specified directory")
    parser.add_argument("folder", nargs = "?", default = ".")
    parser.add_argument("-t", "--types", nargs = "*", default = all_types)
    args = parser.parse_args()
    
    res_list = get_output(args.folder, args.types)
    for res in res_list:
        print(dict2str(res))

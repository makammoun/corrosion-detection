import cv2
import os
import json
from copy import deepcopy
import numpy as np
import random

dir = os.path.join("dataset", "train")


def make_name(name, angle):
    return name[:-4] + '_rotated_' + str(angle) + name[-4:]


def flip_point(x,y,w,h):
    return h - y, x


def flip(img, regions):

    h,w = img.shape[:2]
    center = (w/2, h/2)

    M = cv2.getRotationMatrix2D(center, 90, 1.0)

    img_rotated = cv2.warpAffine(img, M, (h, w))

    img_rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    new_regions = deepcopy(regions)

    for region in regions:
        x,y = regions[region]["shape_attributes"]["all_points_x"], regions[region]["shape_attributes"]["all_points_y"]
        newx, newy = [], []
        for i in range(len(x)):
            xy = flip_point(x[i], y[i], w, h)
            newx.append(xy[0])
            newy.append(xy[1])
        new_regions[region]["shape_attributes"]["all_points_x"] = newx
        new_regions[region]["shape_attributes"]["all_points_y"] = newy

    return img_rotated, new_regions


f = open(os.path.join(dir, "via_region_data.json"), "r")
attr = json.loads(f.read())
f.close()

files = os.listdir(os.path.join(dir))
files.remove("via_region_data.json")
n = len(files)

for i,file in enumerate(files):
    path = os.path.join(dir, file)
    img = cv2.imread(path)
    name = file+str(os.path.getsize(path))

    file90 = make_name(file, 90)
    file180 = make_name(file, 180)
    file270 = make_name(file, 270)

    path90 = os.path.join(dir, file90)
    path180 = os.path.join(dir, file180)
    path270 = os.path.join(dir, file270)

    regions = attr[name]["regions"]

    img90, regions90 = flip(img, regions)
    img180, regions180 = flip(img90, regions90)
    img270, regions270 = flip(img180, regions180)

    cv2.imwrite(path90, img90)
    cv2.imwrite(path180, img180)
    cv2.imwrite(path270, img270)

    size90 = os.path.getsize(path90)
    size180 = os.path.getsize(path180)
    size270 = os.path.getsize(path270)

    entry90 = deepcopy(attr[name])
    entry180 = deepcopy(attr[name])
    entry270 = deepcopy(attr[name])

    entry90['regions'] = regions90
    entry180['regions'] = regions180
    entry270['regions'] = regions270

    entry90['filename'] = file90
    entry180['filename'] = file180
    entry270['filename'] = file270

    entry90['size'] = size90
    entry180['size'] = size180
    entry270['size'] = size270

    key90 = file90 + str(os.path.getsize(path90))
    key180 = file180 + str(os.path.getsize(path180))
    key270 = file270 + str(os.path.getsize(path270))

    attr[key90] = entry90
    attr[key180] = entry180
    attr[key270] = entry270

f = open(os.path.join(dir, "via_region_data.json"),"w")
json.dump(attr, f, sort_keys=True, indent=4)
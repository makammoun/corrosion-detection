"""
    This file tests if the annotation is correct or not
"""
import json
import cv2
import os
import numpy as np

dir = os.path.join("dataset", "train")

f = open(os.path.join(dir, "via_region_data.json"), "r")
attr = json.loads(f.read())
f.close()


files = os.listdir(dir)

for file in files:
    path = os.path.join(dir, file)

    img = cv2.imread(path)
    size = os.path.getsize(path)

    key = file + str(size)

    regions = attr[key]["regions"]

    for region in regions:
        pts = [[x, y] for x,y in zip(regions[region]["shape_attributes"]["all_points_x"],
            regions[region]["shape_attributes"]["all_points_y"])]

        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(0,255,255))

    cv2.imshow("image", img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows()

import os
import shutil
import sys
import argparse
from random import shuffle
import json



def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def write_json(dst, dict):
    f = open(dst, 'w')
    f.write(json.dumps(dict, sort_keys=True, indent=4))
    f.close()

if __name__ == "__main__":

    path = "dataset"
    backup = sys.argv[1]
    annotation = "via_region_data.json"

    params = [int(x) for x in sys.argv[2:]]

    if len(params) == 0:
        params = [70,15,15]
    if sum(params) != 100:
        print("percentages do not sum up to 100%, exiting")
        exit()

    if not os.path.exists(path):
        os.mkdir(path)

    copytree(backup, path)

    # split data
    files = os.listdir(path)
    files.remove(annotation)
    file_paths = [os.path.join(path, file) for file in files]

    f = open(os.path.join(path,annotation), 'r')
    ann = json.loads(f.read())
    f.close()

    shuffle(files)

    train = os.path.join(path, "train")
    test = os.path.join(path, "test")
    val = os.path.join(path, "val")
    os.mkdir(train)
    os.mkdir(test)
    os.mkdir(val)

    size = len(files)
    step1 = int(params[0]/100 * size)
    step2 = int((params[0] + params[1]) / 100 * size)
    train_files = files[:step1]
    val_files = files[step1:step2]
    test_files = files[step2:]


    for file in train_files:
        src = os.path.join(path, file)
        dst = os.path.join(path, "train", file)
        shutil.move(src, dst)
    for file in test_files:
        src = os.path.join(path, file)
        dst = os.path.join(path, "test", file)
        shutil.move(src, dst)
    for file in val_files:
        src = os.path.join(path, file)
        dst = os.path.join(path, "val", file)
        shutil.move(src, dst)

    train_ann, test_ann, val_ann = {},{},{}
    for a in ann:
        name = ann[a]['filename']
        if name in train_files:
            train_ann[a] = ann[a]
        elif name in test_files:
            test_ann[a] = ann[a]
        elif name in val_files:
            val_ann[a] = ann[a]
    
    write_json(os.path.join(path, "train", annotation), train_ann)
    write_json(os.path.join(path, "test", annotation), test_ann)
    write_json(os.path.join(path, "val", annotation), val_ann)
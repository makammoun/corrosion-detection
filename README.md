How to install
==============
- clone and install this package https://github.com/matterport/Mask_RCNN
- install the requirements in ``Mask_RCNN/requirements.txt``
- The scripts use tensorflow 1.x

How to run
==========
Data annotation
---------------
Annotate your dataset here: http://www.robots.ox.ac.uk/~vgg/software/via/via-1.0.6.html<br>
Note: image should be in `.jpg` format

Splitting data
--------------
Place you annotated dataset in a folder with a name different than `dataset` (images + ``via_region_data.json``)<br>
Run ``split.py dataset_folder train_percentage validation_percentage test_percentage`` to split the data into test, train and validation (eg. `split.py original_dataset 70 15 15`, the sum of the three int values have to be 100)<br>
You can run `split.py` without percentages, default values are ``70 15 15``<br>
By default, the original dataset is kept intact, a folder named `dataset` will be created and it will contain the new processed dataset.

Data Augmentation
-----------------
to perform data augmentation, run ``data_augmentation.py``<br>
Data augmentation is performed on `./dataset/train` only

Training
--------
To train run:<br>
``python3 ./corrosion.py train --weights=coco --dataset=./dataset``<br>
This performs training on the pretrained model on the coco dataset

Testing
-------
After training, you can find the latest model in the ``./logs`` folder (eg. ``./logs/damage20200329T2242/mask_rcnn_damage_0010.h5``), perform testing using it<br>
``python3 ./corrosion.py test --weights="latest_model_path" --dataset=./dataset``<br>
This outputs the resulted images in `./output` and displays the score for each image and the mean score

Useful links
============
- Mask_RCNN Repo: https://github.com/matterport/Mask_RCNN
- Online annotator: http://www.robots.ox.ac.uk/~vgg/software/via/via-1.0.6.html
- The script the work is based on: https://github.com/priya-dwivedi/Deep-Learning/blob/master/mask_rcnn_damage_detection/custom.py
"# corrosion-detection" 

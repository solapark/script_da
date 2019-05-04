import random
import os
import shutil
import glob

def write_path_list(path_list, target_file_path):
    target_file = open(target_file_path, 'w')
    for path in path_list :
        target_file.write(path+'\n')
    target_file.close()

source_img_dir = '/data1/sap/SYNTHIA/leftImg8bit/train/'
source_label_dir ='/data1/sap/SYNTHIA/gtFine/train/'
target_img_dir = '/data1/sap/SYNTHIA/leftImg8bit/test/'
target_label_dir ='/data1/sap/SYNTHIA/gtFine/test/'

source_list_path ='/home/sap/dataset/images/cityscapes_pseudo_label/train_cityscapes_pseudo_label_thresh_0.8.txt'
target_list_path ='/home/sap/dataset/images/cityscapes_pseudo_label/test_cityscapes_pseudo_label_thresh_0.8.txt'

all_labels = glob.glob(source_label_dir+'*.png')
#all_labels = os.listdir(source_label_dir)
labels_to_move = random.sample(all_labels, 500)

for label_full_path in labels_to_move :
    label_to_move = label_full_path.split('/')[-1]
    img_to_move =label_to_move.replace(".png", ".png")
    source_label_path =source_label_dir + label_to_move
    source_image_path = source_img_dir + img_to_move
    target_label_path = target_label_dir + label_to_move
    target_image_path = target_img_dir +img_to_move

    shutil.move(source_label_path, target_label_path)
    shutil.move(source_image_path, target_image_path)

'''
source_image_path_list = glob.glob(source_img_dir+'*.jpg')
target_image_path_list = glob.glob(target_img_dir+'*.jpg')
write_path_list(source_image_path_list, source_list_path)
write_path_list(target_image_path_list, target_list_path)
'''

'''
source_dir ='/home/sap/pytorch-CycleGAN-and-pix2pix/datasets/sim10k2cityscapes/trainB/'
target_dir ='/home/sap/pytorch-CycleGAN-and-pix2pix/datasets/sim10k2cityscapes/testB/'
all_source = os.listdir(source_dir)
source_to_move = random.sample(all_source, 100)

for source_name in source_to_move :
    source_path =source_dir+ source_name
    target_path =target_dir + source_name
    shutil.move(source_path, target_path)
'''

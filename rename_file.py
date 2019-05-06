import os
import glob

file_list_name ='/home/sap/dataset/images/fake_cityscapes_2048/fake_cityscapes_2048_train.txt' 
dir = '/home/sap/dataset/images/fake_cityscapes_2048/train/'

name_list = glob.glob(img_dir+'*.jpg')
target_file = open(file_list_name)

for i, name in enumerate(name_list) :
	target_file.write(name+'\n')


target_file.close()
	

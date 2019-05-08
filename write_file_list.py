import os
import glob
from PIL import Image

file_name = '/home/sap/dataset/images/fake_cityscapes_2048/fake_cityscapes_2048_train.txt'
dir = '/home/sap/dataset/images/fake_cityscapes_2048/train/'

name_list = glob.glob(dir+'*.jpg')
list_file = open(file_name, 'w')

for i, name in enumerate(name_list) :
	list_file.write(name + '\n')

list_file.close()

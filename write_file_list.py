import os
import glob
from PIL import Image

file_name = '/home/sap/dataset/images/cityscapes_8class_pseudo/thresh_0_93.txt'
dir = '/home/sap/dataset/images/cityscapes_8class_pseudo/thresh_0_93/'

name_list = glob.glob(dir+'*.jpg')
list_file = open(file_name, 'w')

for i, name in enumerate(name_list) :
	list_file.write(name + '\n')

list_file.close()

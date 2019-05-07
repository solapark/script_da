import os
import glob
from PIL import Image

dir = '/home/sap/dataset/images/fake_cityscapes_2048/train/'

name_list = glob.glob(dir+'*.txt')

for i, name in enumerate(name_list) :
	new_name = name.replace('.txt', '_fake_B.txt')
	os.rename(name, new_name)

	if(i % 100 == 0):
		print(i, '/', len(name_list), 'DONE')

import random
import os
import glob
from utils import * 

choose_num = 100 
#file_dir = '/home/sap/dataset/interpark_data/Kantata300/'
file_dir = '/data1/sap/interpark_data/test/class/28_Kantata_part/'
obj_name_path= '/data1/sap/interpark_data/test/class/video.names'
#img_format = '*.jpg'

names_list = get_list_from_file(obj_name_path)

for name in names_list : 
	img_format = '*' + name + '*.jpg'
	all_images = glob.glob(file_dir+img_format)
	print('deleting', name, 'size:', len(all_images))
	del_num = len(all_images) - choose_num
	images_to_remove = random.sample(all_images, del_num)

	for image_to_remove in images_to_remove :
		label_to_remove = image_to_remove.replace('jpg', 'txt')
		#label_to_remove = label_to_remove.replace('images', 'labels')
		os.remove(image_to_remove)
		#os.remove(label_to_remove)

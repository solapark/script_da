import random
import os
import glob

choose_num = 300
#file_dir = '/home/sap/dataset/interpark_data/Kantata300/'
file_dir = '/home/sap/dataset/interpark_data/Corntea300/'
img_format = '*.jpg'

all_images = glob.glob(file_dir+img_format)
del_num = len(all_images) - choose_num
images_to_remove = random.sample(all_images, del_num)

for image_to_remove in images_to_remove :
    label_to_remove = image_to_remove.replace('jpg', 'txt')
    os.remove(image_to_remove)
    os.remove(label_to_remove)

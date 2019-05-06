import os
from PIL import Image

img_dir = '/home/sap//dataset/images/fake_cityscapes_2048/train'

img_name_list = os.listdir(img_dir)

for i, img_name in enumerate(img_name_list) :
	img_path = img_dir + img_name
	image =Image.open(img_path)	
	resize_image = image.resize((2048, 1024))
	resize_image.save(img_path)

	if(i % 100 == 0):
		print(i, '/', len(img_name_list), 'DONE')

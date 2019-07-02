from utils import get_list_from_file
import shutil

#src_dir = '/data1/sap/download_dataset/clipart/JPEGImages/'
src_dir = '/data1/sap/download_dataset/clipart/Annotations/'
#dst_dir = '/data1/sap/download_dataset/clipart/JPEGImages/test/'
dst_dir = '/data1/sap/download_dataset/clipart/Annotations/test/'
#exp = '.jpg'
exp = '.xml'
file_list_path = '/data1/sap/download_dataset/clipart/ImageSets/Main/test.txt' 
file_list = get_list_from_file(file_list_path)

for file_name in file_list :
	full_src_path = src_dir + file_name + exp
	full_dst_path = dst_dir + file_name + exp

	shutil.move(full_src_path, full_dst_path)

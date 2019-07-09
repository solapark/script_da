import random 
from utils import get_list_from_file

number = 500
src_file_path ='/home/sap/dataset/VOC/test.txt'
dst_file_path = '/home/sap/dataset/VOC/test500.txt'
file_list = get_list_from_file(src_file_path)
samples = random.choices(file_list, k=number)

dst_file = open(dst_file_path, 'w')
for sample in samples :
	dst_file.write(sample+'\n')

dst_file.close()

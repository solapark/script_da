from utils import *

src_file = '/data1/sap/interpark_data/test/label.txt'
dst_file = '/data1/sap/interpark_data/test/label_Corntea_Kantata.txt'

class2class = {\
"0" : "0",\
"28" : "1",\
}

src_lines = get_list_from_file(src_file)
dst_file = open(dst_file, "w")

for line in src_lines :
    file_name, class_num = line.split()
    if class_num in class2class.keys() :
        result_str = file_name + " " + class2class[class_num] + '\n'
    else : 
        result_str = file_name + '\n'
    dst_file.write(result_str)
dst_file.close()

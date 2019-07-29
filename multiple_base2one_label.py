from utils import *

#dst_file = '/data1/sap/interpark_data/test/label.txt'
dst_file = '/data1/sap/interpark_data/test/test.txt'
base_dir = '/home/sap/base/'
dst_dir = '/data1/sap/interpark_data/test/'

base2str = {\
"base001.txt" : "extra_6cam_bot",\
"base002.txt" : "extra_6cam_mid",\
"base003.txt" : "extra_6cam_up",\
"base004.txt" : "large_6cam_bot",\
"base005.txt" : "large_6cam_mid",\
"base006.txt" : "large_6cam_up",\
"base007.txt" : "middle_6cam_bot",\
"base008.txt" : "middle_6cam_mid",\
"base009.txt" : "middle_6cam_up",\
"base010.txt" : "small_6cam_bot",\
"base011.txt" : "small_6cam_mid",\
"base012.txt" : "small_6cam_up"}

dst_file = open(dst_file, "w")

for base_file_name in base2str.keys() :
    base_path = base_dir + base_file_name
    lines = get_list_from_file(base_path)
    print("processing", base_path)
    for line in lines :
        cam_num, frame_num, class_num = line.split()
        file_name = base2str[base_file_name]
        #result_str = dst_dir + file_name + '/video_' + cam_num + "_" + frame_num + '.jpg ' + class_num + '\n'
        result_str = dst_dir + file_name + '/video_' + cam_num + "_" + frame_num + '.jpg' + '\n'
        dst_file.write(result_str)
    print("processing DONE")

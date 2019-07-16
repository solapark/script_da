from utils import *

dst_base_dir = '/data1/sap/interpark_data/test/class/'
src_base_dir = '/data1/sap/interpark_data/test/'
base_dir = '/home/sap/base/'
obj_names_path = '/home/sap/darknet_interpark/181210_test/obj.names'

base2src = {\
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
"base012.txt" : "small_6cam_up",}

names_list = get_list_from_file(obj_names_path)
dst_dir_list = []
for class_num, class_name in enumerate(names_list) :
    class_num_str = str(class_num)
    if class_num<10  : class_num_str = '0'+class_num_str 
    dst_dir = dst_base_dir + class_num_str + '_' + class_name
    dst_dir_list.append(dst_dir)
    makedir(dst_dir)
    print(dst_dir, "generated")

src_file_list = get_file_list_from_dir(base_dir, 'txt')
for src_file_path in src_file_list :
    lines = get_list_from_file(src_file_path)
    src_file_name = get_name_from_path(src_file_path)
    src_dir = src_base_dir + base2src[src_file_name] + '/'
    print("processing", src_file_name)
    for line in lines :
        cam_num, frame_num, class_num = line.split()
        target_name = 'video_' + cam_num + "_" + frame_num + '.jpg'
        src_path = src_dir + target_name
        dst_path = dst_dir_list[int(class_num)] + '/' + target_name
        copy_file(src_path, dst_path)
    print("processing DONE")

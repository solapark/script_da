from utils import * 
import os

label_dir_path ='/home/sap/dataset/clipart/train/labels'
label_dir_name = label_dir_path.split('/')[-1]
obj_names_path = '/home/sap/darknet/clipart/clipart.names'
label_path_list = get_file_list_from_dir(label_dir_path)
obj_names_list = get_list_from_file(obj_names_path)

for obj_idx, obj_name in enumerate(obj_names_list) :
    obj_dir_path = label_dir_path+"_"+obj_name
    obj_label_dir_name = label_dir_name + "_" + obj_name
    if not os.path.exists(obj_dir_path):
        os.makedirs(obj_dir_path)
    print("processing ", obj_label_dir_name)
    for old_label_path in label_path_list :
        new_label_path = old_label_path.replace(label_dir_name, obj_label_dir_name) 
        old_label_lines = get_list_from_file(old_label_path)
        new_label = open(new_label_path, 'w')
        for line in old_label_lines:
            cur_class = line.split(" ")[0]
            if(int(cur_class) == obj_idx) :
                new_line = line.replace(cur_class, '0')
                new_label.write(new_line+'\n')
        new_label.close()
    print("processing DONE")

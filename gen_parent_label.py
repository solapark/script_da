from utils import *

file_list_path = "/data1/sap/interpark_data/test/class/part_label/Kantata_pure_part.txt"
dst_folder = "/data1/sap/interpark_data/test/class/part_label/Kantata_with_parent/"
names_file_path ="/data1/sap/interpark_data/CornTea_Kantata_part/with_parent.names"
base_class_name = "Kantata"
class_id_offset = 1

names_list = get_list_from_file(names_file_path)
def get_idx_from_name(names_list, class_id):
    name = names_list[class_id]
    return int(name.split('_')[1])

def get_class_from_label(label) :
    return int(label.split()[0])

def get_coord_from_label(label) :
    lable_split = label.split()
    center_x, center_y, w, h = float(lable_split[1]), float(lable_split[2]), float(lable_split[3]), float(lable_split[4]) 
    return center_x, center_y, w, h

def get_class_list(labels_list):
    class_list = [get_class_from_label(label) for label in labels_list]
    return class_list

def get_merged_class_id(start_class_id, dst_class_id, class_id_offset) :
    start_idx = get_idx_from_name(names_list, start_class_id)
    dst_idx = get_idx_from_name(names_list, dst_class_id)
    class_name = base_class_name + "_" + str(start_idx) + "_" + str(dst_idx)
    if class_name not in names_list : names_list.append(class_name)
    class_id = names_list.index(class_name)
    print("start_class", names_list[start_class_id], 'dst_class', names_list[dst_class_id], 'class_name', class_name, 'class_id', class_id)
    return class_id

def merge_two_label(names_list, start_idx, src_label, dst_label, class_id_offset) :
    dst_class_id = get_class_from_label(dst_label)
    class_id = get_merged_class_id(start_idx, dst_class_id,class_id_offset) 
    src_center_x, src_center_y, src_w, src_h = get_coord_from_label(src_label)
    dst_center_x, dst_center_y, dst_w, dst_h = get_coord_from_label(dst_label)

    src_x_left = src_center_x - src_w/2.0
    src_x_right = src_center_x + src_w/2.0
    src_y_top = src_center_y - src_h/2.0
    src_y_bottom = src_center_y + src_h/2.0

    dst_x_left = dst_center_x - dst_w/2.0
    dst_x_right = dst_center_x + dst_w/2.0
    dst_y_top = dst_center_y - dst_h/2.0
    dst_y_bottom = dst_center_y + dst_h/2.0

    x_left = min(src_x_left, dst_x_left)
    x_right = max(src_x_right, dst_x_right)
    y_top = min(src_y_top, dst_y_top)
    y_bottom = max(src_y_bottom, dst_y_bottom)

    x_center = (x_left + x_right) / 2.0
    y_center = (y_top + y_bottom) / 2.0
    w = x_right - x_left
    h = y_bottom - y_top 

    label = str(class_id) + " " + str(x_center) + " " + str(y_center) + " " + str(w) + " " + str(h) 
    return label

def make_parent_label(names_list, label_file, start_idx, label, remain_label, class_id_offset):
    if not remain_label : return
    parent_label = merge_two_label(names_list, start_idx, label, remain_label[0], class_id_offset)
    label_file.write(parent_label + '\n')
    make_parent_label(names_list, label_file, start_idx, parent_label, remain_label[1:], class_id_offset)

file_list = get_list_from_file(file_list_path)
names_list = get_list_from_file(names_file_path)

for file_path in file_list :
    print(file_path)
    file_name = get_name_from_path(file_path)
    dst_path = dst_folder + file_name

    copy_file(file_path, dst_path)
    dst_file = open(dst_path, 'a')

    old_labels = get_list_from_file(file_path)
    class_list = get_class_list(old_labels)
    old_labels = [sorted_old_label for _,sorted_old_label in sorted(zip(class_list, old_labels))]

    for i, label in enumerate(old_labels) :
        start_class_id =get_class_from_label(label) 
        make_parent_label(names_list, dst_file, start_class_id, label, old_labels[i+1:], class_id_offset)
        #make_parent_label(names_list, dst_file, i, label, old_labels[i+1:], class_id_offset)

    dst_file.close()
    
write_list_in_file(names_file_path, names_list)

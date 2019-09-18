import glob
import os
import shutil

def get_file_list_from_dir(dir_path, exp='', is_full_path = True):
    #use : get_file_list_from_dir("/home/sap", "png")
    file_form = dir_path + '/*' 
    if(exp):
        file_form += '.'+exp 
    file_list = glob.glob(file_form)
    if not is_full_path :
        new_file_list = [get_name_from_path(cur_file) for cur_file in file_list]
        file_list = new_file_list
    return file_list

def get_unique_file_list_from_multiple_dir(base_path, folder_list) :
    file_set = set()
    for folder in folder_list :
        file_list = get_file_list_from_dir(base_path + folder, is_full_path = False)
        file_set = (file_set | set(file_list))
    return list(file_set)

def get_list_from_file(file_path):
    list_file = open(file_path, 'r')
    target_list = list_file.read().strip().splitlines()
    list_file.close()
    return target_list

def get_name_from_path(path):
    name = path.split('/')[-1]
    return name

def check_path_exist(path) :
    if os.path.exists(path):
        return True 
    else :
        return False
 
def makedir(path):
    if not check_path_exist(path):
        os.makedirs(path)

def copy_file(src_path, dst_path) :
    shutil.copy(src_path, dst_path)

def move_file(src_path, dst_path) :
    shutil.move(src_path, dst_path)

def write_list_in_file(file_path, target_list) :
    target_file = open(file_path, 'w')
    for item in target_list :
        target_file.write(item + '\n')
    target_file.close()


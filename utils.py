import glob
import os

def get_file_list_from_dir(dir_path, exp=''):
    #use : get_file_list_from_dir("/home/sap", "png")
    file_form = dir_path + '/*' 
    if(exp):
        file_form = '.'+exp 
    file_list = glob.glob(file_form)
    return file_list

def get_list_from_file(file_path):
    list_file = open(file_path, 'r')
    target_list = list_file.read().strip().splitlines()
    list_file.close()
    return target_list

def get_name_from_path(path):
    name = path.split('/')[-1]
    return name

def makedir(path):
	if not os.path.exists(path):
		os.makedirs(path)


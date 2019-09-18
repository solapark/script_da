from utils import *

base_path = "/data1/sap/interpark_data/test/class/part_label/"
new_folder = "Kantata_pure_part/"

names_file_path =base_path + new_folder.split('/')[0] + ".names"
folder_list = get_list_from_file(names_file_path)
file_list = get_unique_file_list_from_multiple_dir(base_path, folder_list)
makedir(base_path + new_folder)

for file_name in file_list :
    new_path = base_path + new_folder + file_name
    new_file = open(new_path, 'w')
    for i, folder in enumerate(folder_list) :
        old_path = base_path +  folder + "/" + file_name
        if not check_path_exist(old_path) : continue
        old_lines = get_list_from_file(old_path)
        for old_line in old_lines :
            new_class =str(i) + " " 
            new_line = old_line.replace("0 ", new_class, 1)
            new_file.write(new_line + '\n')
    new_file.close()

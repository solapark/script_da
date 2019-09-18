from utils import *

dot_data_dir = '/home/sap/darknet/clipart/'
dot_data_format = "pseudo_clipart_"
dot_names_path = '/home/sap/darknet/clipart/one_class.names'
labels_path = '/home/sap/dataset/clipart/train/'
target_name_list_path = '/home/sap/darknet/clipart/clipart.names'
target_list = get_list_from_file(target_name_list_path)

def make_dot_data_file(dot_data_path, dot_names_path, obj) : 
    _file  = open(dot_data_path, 'w')
    wording = 'names = {dot_names_path}\n' +\
            'label_dir = /pseudo_labels_{obj}/'
    wording = wording.format(dot_names_path = dot_names_path, obj = obj)
    _file.write(wording)
    _file.close()

for i, obj in enumerate(target_list) :
    dot_data_path = dot_data_dir + dot_data_format + obj + ".data"
    make_dot_data_file(dot_data_path, dot_names_path, obj)
    labels_dir = labels_path + "pseudo_labels_" + obj
    makedir(labels_dir)

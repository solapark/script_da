from utils import *

dot_data_dir = '/home/sap/darknet/VOC/'
dot_names_dir = dot_data_dir
train_dot_data_format = "VOC_"
test_dot_data_format = "test_clipart_"
dot_names_format = "VOC_"
backup_dir_format = "/data1/sap/backup/clipart2VOC/VOC_"

target_name_list_path = '/home/sap/darknet/VOC/VOC.names'
target_list = get_list_from_file(target_name_list_path)

def make_train_dot_data_file(train_dot_data_path, dot_names_path, obj, backup_dir) : 
    _file  = open(train_dot_data_path, 'w')
    wording = 'classes = 1\n' + \
            'train = /home/sap/dataset/VOC/train.txt\n' +\
            'valid = /home/sap/dataset/VOC/test500.txt\n' +\
            'names = {dot_names_path}\n' +\
            'backup = {backup_dir}\n' +\
            'label_dir = /labels_{obj}/'
    wording = wording.format(dot_names_path = dot_names_path, obj = obj, backup_dir = backup_dir)
    _file.write(wording)
    _file.close()

def make_test_dot_data_file(test_dot_data_path, obj) :
    _file  = open(test_dot_data_path, 'w')
    wording = "classes = 1\n" + \
            "train = /home/sap/dataset/clipart/train.txt\n" +\
            "valid = /home/sap/dataset/clipart/test.txt\n" +\
            "names = /home/sap/darknet/clipart/clipart.names\n" +\
            "backup = /data1/sap/backup/clipart2VOC/clipart\n" +\
            "label_dir = /labels_{obj}/"
    wording = wording.format(obj = obj)
    _file.write(wording)
    _file.close()

def make_dot_names_file(dot_names_path, obj) :
    _file  = open(dot_names_path, 'w')
    _file.write(obj)
    _file.close()

for i, obj in enumerate(target_list) :
    train_dot_data_path = dot_data_dir + train_dot_data_format + obj + ".data"
    test_dot_data_path = dot_data_dir + test_dot_data_format + obj + ".data"
    dot_names_path = dot_names_dir + dot_names_format + obj + ".names"
    backup_dir_path = backup_dir_format + obj

    make_train_dot_data_file(train_dot_data_path, dot_names_path, obj, backup_dir_path)
    make_test_dot_data_file(test_dot_data_path, obj)
    make_dot_names_file(dot_names_path, obj)
    makedir(backup_dir_path)

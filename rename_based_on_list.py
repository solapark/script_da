from utils import get_list_from_file, get_name_from_path
import sys
import shutil

source_path ='/home/sap/dataset/images/fake_cityscapes_2048/train'
target_path ='/home/sap/dataset/images/fake_cityscapes_2048/train'

def rename_based_on_list(argv):
    if(len(argv) > 1): 
        source_path =argv[1]
        target_path =argv[2]

    source_list = get_list_from_file(source_path)
    target_list = get_list_from_file(target_path)

    for source, target in zip(source_list, target_list) :
        source_name = get_name_from_path(source)
        target_name = get_name_from_path(target)
    
        old_source = source
        new_source = source.replace(source_name, target_name)
    
        shutil.move(old_source, new_source)

if __name__ == "__main__":
    rename_based_on_list(sys.argv)

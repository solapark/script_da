from utils import get_list_from_file, get_name_from_path
import sys
import shutil
import random

source_path ='/data1/sap/cyclegan_interpark/dataset/Corntea_Kantata_640/trainB.txt'
target_path ='/data1/sap/cyclegan_interpark/dataset/Corntea_Kantata_640/trainA.txt'
random_list = 1

def rename_based_on_list(argv):
    source_list = get_list_from_file(source_path)
    target_list = get_list_from_file(target_path)
    if(random_list) :
        random.shuffle(source_list)
        random.shuffle(target_list)

    for source, target in zip(source_list, target_list) :
        source_name = get_name_from_path(source)
        target_name = get_name_from_path(target)
    
        old_source = source
        new_source = source.replace(source_name, target_name)
    
        shutil.move(old_source, new_source)

if __name__ == "__main__":
    rename_based_on_list(sys.argv)

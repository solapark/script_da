import os
import glob
import shutil

dir = '/home/sap/dataset/images/fake_cityscapes_2048/train/'

#name_list = glob.glob(dir+'*.txt')
name_list = glob.glob(dir+'*.png')

for i, old_name in enumerate(name_list) :
    #new_name = old_name.replace(".txt", "_fake_B.txt")  
    new_name = old_name.replace(".png", ".jpg")  
    shutil.move(old_name, new_name)

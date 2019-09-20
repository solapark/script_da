import cv2
from utils import *
import numpy as np

file_list_path = '/data1/sap/interpark_data/CornTea_Kantata_cam0.txt'
new_folder = "/data1/sap/interpark_data/CornTea_Kantata_stereo/"
w = 640
h = 360
c = 3

if not check_path_exist(new_folder): makedir(new_folder)
cam0_paths = get_list_from_file(file_list_path)
cnt = np.zeros(6)
for cam0_path in cam0_paths :
    for i in range(0, 6) :
        read_path = cam0_path.replace('_0_', '_'+str(i)+'_')
        save_name = get_name_from_path(read_path)
        save_path =new_folder + save_name 
        if check_path_exist(read_path):
            save_img = cv2.imread(read_path)
        else : 
            save_img = np.zeros(shape = (h,w,c))
            cnt[i] += 1
            print("black : ", save_path)
        cv2.imwrite(save_path, save_img)            

print('black cnt', cnt)

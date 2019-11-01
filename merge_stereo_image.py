import cv2
from utils import *
import numpy as np

file_list_path = '/data1/sap/interpark_data/CornTea_Kantata_cam0.txt'
new_folder = "/data1/sap/interpark_data/CornTea_Kantata_test/"

cam0_paths = get_list_from_file(file_list_path)

for cam0_path in cam0_paths :
    result_img = cv2.imread(cam0_path)
    cam0_shape = result_img.shape
    for i in range(1, 6) :
        to_paste_img_path = cam0_path.replace('_0_', '_'+str(i)+'_')
        if check_path_exist(to_paste_img_path):
            to_paste_img = cv2.imread(to_paste_img_path)
        else : 
            to_paste_img = np.zeros(shape = cam0_shape)
        result_img = np.append(result_img, to_paste_img, axis=2)
    cam0_name = get_name_from_path(cam0_path)
    save_path =new_folder + cam0_name 
    #cv2.imwrite(save_path, result_img)
    np.save(save_path, result_img)

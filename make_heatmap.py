import cv2
import numpy as np
import glob
import re
from utils import *

folder_path = '/home/sap/darknet_interpark/activation_map/'
save_folder = '/home/sap/darknet_interpark/activation_map/result/'
img_size = (416, 416)

def get_file_name_from_layer_num(layer_num):
    name_patten = '.*layer-'+str(layer_num)+'.*'
    return name_patten


def check_pattern_match(file_name, keyword):
    is_match = False
    pattern = re.compile(keyword)
    if pattern.match(file_name) : is_match = True 
    return is_match

def merge_img(result_img, cur_img):
    if result_img.any() :
        result_img += cur_img
    else :
        result_img = cur_img
    return result_img

def get_norm_img(img):
    max_val = img.max()
    norm_img = img/max_val * 255.0
    norm_img = norm_img.astype(np.uint8)
    return norm_img

activation_list = glob.glob(folder_path+'*.jpg')
activation_list.sort()
heat_bf_norm_list = []
layer_num = 0 
slice_list = []
makedir(save_folder)

while (activation_list) :
    name_pattern = get_file_name_from_layer_num(layer_num)
    result_img = np.array([]) 
    save_path = save_folder +  str(layer_num) + '.jpg'
    layer_num += 1
    for activation_map_path in activation_list :
        if check_pattern_match(activation_map_path, name_pattern):
            cur_img = cv2.imread(activation_map_path)
            result_img = merge_img(result_img, cur_img)
            activation_list = activation_list[1:]
        else :
            norm_img = get_norm_img(result_img)
            cv2.imwrite(save_path, norm_img)
            break

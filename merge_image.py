import cv2
from utils import *
import numpy as np
import re

folder_path = '/home/sap/darknet_interpark/activation_map/'
save_folder = '/home/sap/darknet_interpark/activation_map/heatmap/'
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

def get_heatmap(img) :
    return cv2.applyColorMap(img, cv2.COLORMAP_JET)

def get_layer_num(path) :
    name_patten = '.*layer-(.*)_slice.*'
    patten = re.compile(name_patten)
    matchobj = patten.search(path)
    return int(matchobj.group(1))

activation_list = glob.glob(folder_path+'*.jpg')
activation_list.sort()
heat_bf_norm_list = []
layer_num = get_layer_num(activation_list[0])
slice_list = []
makedir(save_folder)
all_merge_img = np.array([]) 

while activation_list :
    name_pattern = get_file_name_from_layer_num(layer_num)
    result_img = np.array([]) 
    save_path = save_folder + 'heatmap_layer_' + str(layer_num) + '.jpg'
    for activation_map_path in activation_list :
        if check_pattern_match(activation_map_path, name_pattern):
            cur_img = cv2.imread(activation_map_path)
            result_img = merge_img(result_img, cur_img)
            '''
            cv2.imshow("cur_img", cur_img)
            cv2.imshow("result_img", result_img)
            cv2.waitKey(0)
            '''
            activation_list = activation_list[1:]
        else :
            print(layer_num)
            norm_img = get_norm_img(result_img)
            norm_img = cv2.resize(norm_img, img_size, interpolation = cv2.INTER_NEAREST)
            heatmap = get_heatmap(norm_img)
            cv2.imwrite(save_path, heatmap)
            #cv2.imwrite(save_path, norm_img)
            layer_num = get_layer_num(activation_list[0])

            result_img_resized = cv2.resize(result_img, img_size, interpolation = cv2.INTER_NEAREST)
            all_merge_img = merge_img(all_merge_img, result_img_resized)
            break

all_norm_img = get_norm_img(all_merge_img)
heatmap = get_heatmap(all_norm_img)
save_path = save_folder + 'heatmap.jpg'
cv2.imwrite(save_path, heatmap)





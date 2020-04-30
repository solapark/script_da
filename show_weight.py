import cv2
from utils import *
import numpy as np
import re

file_base_path = '/home/sap/darknet_interpark/activation_map/wgt/Layer_'
ext = 'jpg'

channel_base_path = '/home/sap/darknet_interpark/activation_map/gt_c_pred_k/'

save_folder = 'priority_heatmap'

layer_idx_list = [81, 93, 105]
save_num = 6

resize_size = (416, 416)
class_list = ['corntea', 'kantata']
anchor_size = 3
final_layer_size = 21

def get_filter_idx_list(final_layer_size, anchor_size):
    kernel_list = list(range(final_layer_size))
    one_anchor_size = final_layer_size / anchor_size #7
    filter_idx_list = [i for i in kernel_list if i%one_anchor_size-5 >= 0]
    return filter_idx_list

def get_class_name(class_list, kernel_idx,  final_layer_size, anchor_size):
    one_anchor_size = int(final_layer_size / anchor_size) #7
    idx = kernel_idx % one_anchor_size % 5
    class_name = class_list[idx]
    return  class_name

def get_anchor_idx(kernel_idx, final_layer_size, anchor_size):
    one_anchor_size = int(final_layer_size / anchor_size) #7
    return int(kernel_idx/one_anchor_size)

def get_channel_path(channel_base_path, layer_idx, channel_idx):
    channel_path = channel_base_path + 'layer-'+str(layer_idx) + '_slice-'+str(channel_idx)+'.jpg' 
    return channel_path

if __name__ == '__main__' :
    makedir(channel_base_path + save_folder)
    filter_idx_list = get_filter_idx_list(final_layer_size, anchor_size)
    for layer_idx in layer_idx_list :
        file_full_path = file_base_path + str(layer_idx) + '.' + ext
        img = cv2.imread(file_full_path, cv2.IMREAD_GRAYSCALE)
        print('layer', layer_idx, img.shape)
        for i, filter_idx in enumerate(filter_idx_list) :
            print(i, ':',  filter_idx)
            filter_weight = img[filter_idx]
            #print(filter_weight)
            idx_list = list(range(len(filter_weight)))
            _, sorted_idx = zip(*sorted(zip(filter_weight, idx_list), reverse = True))
            #print(sorted_idx)
            sorted_idx = sorted_idx[0:save_num]
            for j, channel_idx in enumerate(sorted_idx) :
                channel_path = get_channel_path(channel_base_path, layer_idx-1, channel_idx)
                channel_name = get_name_from_path(channel_path)
                class_name = get_class_name(class_list, filter_idx,  final_layer_size, anchor_size)
                anchor_idx = get_anchor_idx(filter_idx, final_layer_size, anchor_size)
                save_name = 'layer_' + str(layer_idx) + '_anchor_' + str(anchor_idx) + '_' + class_name + '_' + str(j) + 'th_wgt'+str(filter_weight[channel_idx])+'_slice_'+ str(channel_idx)
                #save_name = str(j) + 'th_wgt'+str(filter_weight[channel_idx])+'_'+ channel_name
                save_path = channel_base_path + '/' + save_folder + '/' + save_name + '.jpg'

                channel = cv2.imread(channel_path,cv2.IMREAD_GRAYSCALE)
                channel_resized = cv2.resize(channel, resize_size, interpolation = cv2.INTER_NEAREST)
                cv2.imshow(save_name, channel_resized)
                #cv2.imwrite(save_path, channel)
                cv2.waitKey(0)

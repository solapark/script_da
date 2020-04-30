import cv2
import numpy as np
import argparse
import sys

#channel_base_path = '/home/sap/darknet_interpark/activation_map/gt_k_pred_k/2_53'
channel_base_path = '/home/sap/darknet_interpark/activation_map/tmp'
n_th_layer = 1
#row = 0
#col =3

layer_idx_list = [80, 92, 104]
channel_size_list = [1024, 512, 256]

def get_channel_path(channel_base_path, layer_idx, channel_idx):
    channel_path = channel_base_path + '/layer-'+str(layer_idx) + '_slice-'+str(channel_idx)+'.jpg' 
    return channel_path

if __name__ == '__main__' :
    row = int(sys.argv[1])
    col = int(sys.argv[2])
    layer_idx = layer_idx_list[n_th_layer]
    channel_size = channel_size_list[n_th_layer]
    #print(channel_base_path, 'layer', n_th_layer, 'row', row, 'col', col)
    for i in range(channel_size):
        channel_path = get_channel_path(channel_base_path, layer_idx, i)
        channel = cv2.imread(channel_path,cv2.IMREAD_GRAYSCALE)
        print(channel[row, col], end = ' ')

import argparse 
import sys
import matplotlib.pyplot as plt
import sys
import re
import random
import numpy as np

def get_network_name_from_loss_path(file_path):
#file_path = "pathToFile/loss_networkName.log"
    #target = '.*loss_().log'
    #regex = re.compile(target)
    regex = re.compile(r'.*loss_(.*).log')
    matchobj = regex.search(file_path)
    return  matchobj.group(1)

def get_testTarget_from_map_path(file_path):
#file_path = "pathToFile/map_testTarget_with_networkName.log"
    target = '.*map_(.*)_with_'
    regex = re.compile(target)
    matchobj = regex.search(file_path)
    return  matchobj.group(1)


def extract_loss_list(file_path) :
    f = open(file_path)
    lines  = [line.rstrip("\n") for line in f.readlines()]
    
    numbers = {'1','2','3','4','5','6','7','8','9'}

    iters = []
    loss = []
    
    for line in lines:
        word = line.split(' ')
        if len(word) > 4 and word[1][-1:]==':' and word[1][0] in numbers :
            iters.append(int(word[1][:-1]))            
            loss.append(float(word[3]))

    return (iters, loss)

def plot_loss(file_path, loss_ax, iters, loss):
#file_path = "pathToFile/loss_networkName.log"
    loss_ax.plot(iters,loss, color = 'y', label = 'loss')
    if(len(loss)):
        ylim = min(max(loss)*1.2, min(loss)+2)
    else :
        ylim = 1
    loss_ax.set_ylim(0, ylim)
    loss_ax.set_ylabel('loss')

    loss_ax.grid()
    loss_ax.legend()

def plot_map(file_path, map_ax, color):
#file_path = "pathToFile/map_testTarget_with_networkName.log"
    test_target = get_testTarget_from_map_path(file_path)
    label = 'map_' + test_target + '(%)'

    map_iters = []
    map_values = []

    f = open(file_path)
    lines  = [line.rstrip("\n") for line in f.readlines()]
    
    for line in lines:
        word = line.split(' ')
        if word[0]=='#' :
            weight_path = word[-1]
            weight_token = weight_path.split('_')[-1]
            weight_num = weight_token.split('.')[0]
            map_iters.append(int(weight_num))            

        if len(word) > 1 and word[1]=='mean':
            map_token = word[6]
            map_value = map_token.split(',')[0]
            map_values.append(float(map_value)*100)

    map_iters,map_values = zip(*sorted(zip(map_iters,map_values)))
    
    map_ax.plot(map_iters, map_values, marker = 'o', color=color, label = label)
    map_ax.set_ylabel(label)

    for x, y in zip(map_iters, map_values):
        label = "{:.2f}".format(y)
        map_ax.annotate(label, (x,y), textcoords="offset points", xytext=(0,0), ha = 'center')
    
    map_ax.legend()
 
def main(argv):
    loss_path = argv[1]
    map_path_list = []
    if(len(argv) > 2) :
        for i in range(2, len(argv)):
            map_path_list.append(argv[i])

    whole_loss_ax = plt.subplot(2,1,1)

    network_name =get_network_name_from_loss_path(loss_path) 
    whole_iter_title = network_name+' whole iters'
    whole_loss_ax.set_title(whole_iter_title)
    whole_loss_ax.set_xlabel('iters')
    whole_iters, whole_loss = extract_loss_list(loss_path)
    plot_loss(loss_path, whole_loss_ax, whole_iters, whole_loss)

    last_loss_ax = plt.subplot(2,1,2)

    num_of_iters = 200
    last_loss_ax.set_title("%s last %s iters" %(network_name, num_of_iters))
    last_iters = whole_iters[-num_of_iters : ]
    last_loss = whole_loss[-num_of_iters : ]
    plot_loss(loss_path, last_loss_ax, last_iters, last_loss)

    if(map_path_list) :
        map_ax = whole_loss_ax.twinx()
        #cmap = plt.cm.get_cmap('hsv', len(map_path_list))
        if(len(map_path_list) == 1):
            color_interval = 1.0-0.01
        else :
            color_interval = (1.0-0.01)/(len(map_path_list)-1)
        for i, map_path in enumerate(map_path_list) :
            color_offset =color_interval * i
            color = (color_offset, 0.5,0.5)
            plot_map(map_path, map_ax, color)

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main(sys.argv)

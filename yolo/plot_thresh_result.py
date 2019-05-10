import argparse 
import sys
import matplotlib.pyplot as plt
import sys
import re
import numpy as np

def get_network_name_from_path(file_path):
#file_path = "pathToFile/thresh_result_networkName_with_networkName.log"
    target = '.*thresh_result_(.*_with_.*).log'
    regex = re.compile(target)
    matchobj = regex.search(file_path)
    return  matchobj.group(1)


def extract_thresh_result(file_path):
    f = open(file_path)
    lines  = [line.rstrip("\n") for line in f.readlines()]
    
    thresh_list = []
    result_list = []

    target = '^ for thresh = (.*), TP = (.*), FP = (.*), FN = (.*), average IoU = (.*) % $'

    for line in lines:
        regex = re.compile(target)
        matchobj = regex.search(line)

        if(matchobj):
            thresh = float(matchobj.group(1))
            TP = int(matchobj.group(2))
            FP = int(matchobj.group(3))
            FN = int(matchobj.group(4))
            IOU = float(matchobj.group(5))
            result = {'TP': TP, 'FP': FP, 'FN': FN, 'IOU': IOU}

            thresh_list.append(thresh)
            result_list.append(result)

    f.close()

    thresh_list, result_list = zip(*sorted(zip(thresh_list, result_list)))
    return (thresh_list, result_list)

def get_result_from_0_to_target(result_list):
    result_0_to_target_list = []
    thresh_0_result = result_list[0]

    for i, result in enumerate(result_list) :
        TP_diff = thresh_0_result['TP'] - result['TP']
        FP_diff = thresh_0_result['FP'] - result['FP'] 

        result_0_to_target = {'TP': TP_diff, 'FP': FP_diff}     
        result_0_to_target_list.append(result_0_to_target)
         
    return result_0_to_target_list  

def get_target_list(result_list, target):
    target_list = [result[target] for result in result_list]
    return target_list

def plot_TP_FP_bar(ax, thresh_list, TP_list, FP_list):
    width = 0.01
    ax.bar(thresh_list, TP_list, color = 'lightgreen', width = width, label = 'TP', bottom = FP_list)
    ax.bar(thresh_list, FP_list, color = 'lightcoral', width = width, label = 'FP')
    ax.set_ylabel('TP, FP', rotation=0, labelpad=20)
    TP_FP = [TP+FP for TP, FP in zip(TP_list, FP_list)]
    ax.set_ylim(0, max(TP_FP))
    #ax.set_yticks(np.arange(0, max(TP_FP), 1))
    ax.legend()

def plot_TP_FP_ratio(ax, thresh_list, TP_list, FP_list, title):
    if(title == 'TP/FP'):
        TP_FP_ratio = [ float(TP) / float(FP) if FP != 0 else 0 for TP, FP in zip(TP_list, FP_list) ]
        ax.plot(thresh_list, TP_FP_ratio, label = title, color = 'k')
    elif(title == 'FP/TP'):
        TP_FP_ratio = [ float(FP) / float(TP) if TP != 0 else 0 for TP, FP in zip(TP_list, FP_list) ]
        ax.plot(thresh_list, TP_FP_ratio, label = title, color = 'k')
    ax.set_ylabel(title, rotation=0, labelpad=20)
    ax.set_ylim(0, max(TP_FP_ratio))
    ax.legend()

def plot_result(ax, thresh_list, result_list, title):
    TP = get_target_list(result_list, 'TP')
    FP = get_target_list(result_list, 'FP')

    plot_TP_FP_bar(ax, thresh_list, TP, FP)

    ax.set_xlabel('threshold')
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_xlim(0, 1)
    ax.set_title(title)

    ratio_ax = ax.twinx()
    if(title == '0 ~ thresh'):
        plot_TP_FP_ratio(ratio_ax, thresh_list, TP, FP, 'FP/TP')
    elif(title == 'thresh ~ 1'):
        plot_TP_FP_ratio(ratio_ax, thresh_list, TP, FP, 'TP/FP')

    ratio_ax.grid()

def main(argv):
    file_path = argv[1]

    result_0_to_target_ax = plt.subplot(2,1,1)
    result_target_to_1_ax = plt.subplot(2,1,2)

    thresh_list, result_list = extract_thresh_result(file_path)
    reuslt_0_to_target_list = get_result_from_0_to_target(result_list)

    plot_result(result_0_to_target_ax, thresh_list, reuslt_0_to_target_list, '0 ~ thresh')
    plot_result(result_target_to_1_ax, thresh_list, result_list, 'thresh ~ 1')

    whole_title = get_network_name_from_path(file_path)
    plt.suptitle(whole_title)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main(sys.argv)

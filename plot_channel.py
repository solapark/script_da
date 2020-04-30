from utils import get_list_from_csv
import matplotlib.pyplot as plt

csv_path = "/home/sap/darknet_interpark/activation_map/tmp/data/channel_value.csv"
name_list = ['gt_c_pred_c', 'gt_c_pred_k', 'gt_k_pred_c', 'gt_k_pred_k']
color_list = [ 'r','b', 'g', 'c']
show_size = 50

if __name__ == '__main__' :
    data = get_list_from_csv(csv_path)
    header = data[0]
    data = data[1:]
    channel_idx = header[2:][:show_size]
    #channel_idx = header[2:]
    channel_idx = list(map(int, channel_idx) )
    fg, ax = plt.subplots()
    for d in data :
        name = d[1] 
        if(name != 'gt_c_pred_c' and name != 'gt_c_pred_k') : continue
        color = color_list[name_list.index(name)]
        value = d[2:][:show_size]
        #value = d[2:]
        value = list(map(int, value))
        ax.plot(channel_idx, value, color, marker='o', linestyle='', alpha=.1)
        #plt.show()

    #ax.legend(fontsize=12, loc='upper left')
    #plt.legend(name_list, loc='upper left')
    plt.title('result')
    plt.xlabel("channel")
    plt.ylabel("value")
    plt.yticks(list(range(0, 255, 50)))
    plt.xticks(list(range(0, show_size, 2)))
    plt.grid()
    plt.show()

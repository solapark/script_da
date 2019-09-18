from utils import *
import sys
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels

#data_name = 'Corntea_Kantata_deep_part3'
#data_name = 'Corntea_Kantata_pure_part'
#data_name = 'Corntea_Kantata_600_with_parent'
data_name = 'Corntea_Kantata_600_org'
iteration = '8000'
base_dir = '/home/sap/darknet_interpark/'
#base_dir = '/home/sap/darknet_partdet/'
#base_dir = '/home/sap/darknet_partdet_tmp/'

#gt_file ='/data1/sap/interpark_data/test/label_Corntea_Kantata.txt'
gt_file ='/data1/sap/interpark_data/test/label_Corntea_Kantata_pure.txt'
gt_names_file = '/home/sap/darknet_interpark/Corntea_Kantata/obj.names'
#detection_file ='/home/sap/darknet_interpark/' + data_name + '/classification_result/' + data_name + '_' + iteration +'.log'
detection_file =base_dir + data_name + '/classification_result/' + iteration +'.log'
detection_names_file = base_dir + data_name + '/obj.names'

def get_title_from_log_file(detection_file, data_name):
    log_file_full_name = detection_file.split('/')[-1]
    log_file_name = log_file_full_name.split('.')[0]
    log_file_name_split = log_file_name.split('_')
    #log_file_name_wo_weight = '_'.join(log_file_name_split[:-1])
    weight_iter = log_file_name_split[-1]
    #title = log_file_name_wo_weight + ' @' +weight_iter
    title = data_name + ' @' +weight_iter
    return title


def plot_confusion_matrix(y_true, y_pred, classes, gt_idx, det_idx, double_box_idx, bg_idx, 
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels = list(range(len(classes))))

    cm_gt_class = cm[gt_idx]
    cm_gt_bg = cm[bg_idx]
    cm_gt_final = np.append(cm_gt_class, cm_gt_bg, axis = 0)

    cm_det_gt = cm_gt_final[:, gt_idx]
    cm_det_class = cm_gt_final[:, det_idx]
    cm_det_double_box =cm_gt_final[:, double_box_idx] 
    cm_det_bg = cm_gt_final[:, bg_idx]
    cm_det_final = np.append(cm_det_gt, cm_det_class, axis = 1)
    cm_det_final = np.append(cm_det_final, cm_det_double_box, axis = 1)
    cm_det_final = np.append(cm_det_final, cm_det_bg, axis = 1)

    cm = cm_det_final

    # Only use the labels that appear in the data
    gt_class = classes[gt_idx]
    det_class = classes[det_idx]
    double_class = classes[double_box_idx]
    bg_class = classes[bg_idx]
    yticklabel = np.array(gt_class  + bg_class)
    #xticklabel = np.array(det_class + double_class+ bg_class)
    xticklabel = np.array(gt_class + det_class + double_class+ ['real_obj'])

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=xticklabel, yticklabels=yticklabel,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    #fig.tight_layout()
    return ax


gt_names_list = get_list_from_file(gt_names_file)
detection_names_list = get_list_from_file(detection_names_file)
names_list = gt_names_list + detection_names_list
double_box_list = [det_name + '_double_box' for det_name in detection_names_list]
names_list = names_list + double_box_list + ['bg']
names_size = len(names_list)
gt_names_size = len(gt_names_list)
det_names_size = len(detection_names_list)
det_start_idx = gt_names_size
double_box_start_idx = gt_names_size + det_names_size
bg_idx = names_size - 1

cm_truth = list()
cm_pred = list()

label_lines = get_list_from_file(gt_file)
detection_lines = get_list_from_file(detection_file)

for label_line, detection_line in zip(label_lines, detection_lines) :
    label_line_split = label_line.split()
    truth_file_name = label_line_split[0]
    if(len(label_line_split) == 1) :
        truth_class = bg_idx
    else :
        truth_class = int(label_line_split[1])

    detection_line_split = detection_line.split()
    detection_file_name = detection_line_split[0]
    if(truth_file_name !=detection_file_name):
        print(truth_file_name, "!=", detection_file_name)
        sys.exit(1)
    detection_classes = detection_line_split[1:]

    ''' 
    if '1' in detection_classes :
        if any(det in ['2','3','4','5','6'] for det in detection_classes) : detection_classes = [det.replace('1', '0') for det in detection_classes]
    '''
  
    double_box = [0] * det_names_size
    is_found = [0] * (gt_names_size+1)
    for detection_class in detection_classes :
        detection_class = int(detection_class)
        #if(detection_class ==11) : continue
        cm_truth.append(truth_class)
        real_detection_class = det_start_idx  + detection_class
        if not double_box[detection_class] :
            double_box[detection_class] = 1
            cm_pred.append(real_detection_class)
        else :
            double_box_idx = double_box_start_idx + detection_class
            cm_pred.append(double_box_idx)

        parrent_class = detection_names_list[detection_class].split('_')[0]
        parrent_class_idx = gt_names_list.index(parrent_class)
        if not is_found[parrent_class_idx] :
            is_found[parrent_class_idx] = 1
            cm_truth.append(truth_class)
            cm_pred.append(parrent_class_idx)
    #if not is_found[truth_class] :
    cm_truth.append(truth_class)
    cm_pred.append(bg_idx)


gt_idx = slice(0, gt_names_size)
det_idx = slice(det_start_idx, double_box_start_idx)
double_box_idx = slice(double_box_start_idx, bg_idx)
bg_idx = slice(bg_idx, None)
title = get_title_from_log_file(detection_file, data_name)
print(confusion_matrix(cm_truth, cm_pred, labels=list(range(names_size))))
plot_confusion_matrix(cm_truth, cm_pred, names_list, gt_idx, det_idx, double_box_idx, bg_idx, title=title)

plt.rcParams["figure.figsize"] = (500, 500)
#plt.figure(figsize= (50, 50))
plt.savefig('test.png')
plt.show()

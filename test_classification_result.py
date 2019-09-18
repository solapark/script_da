from utils import *
import sys
import numpy as np

'''
gt_file ='/data1/sap/interpark_data/test/label.txt'
detection_file ='/home/sap/darknet_interpark/181210_test/classfication_result/base_120000.log'
result_file_path ='/home/sap/darknet_interpark/181210_test/map/base_120000.log'
names_file ='/home/sap/darknet_interpark/181210_test/obj.names' 
'''
'''
detection_file = '/home/sap/darknet_interpark/Corntea_Kantata/classification_result/Corntea_Kantata_4000.log'
result_file_path ='/home/sap/darknet_interpark/Corntea_Kantata/map/Corntea_Kantata_4000.log'
gt_file ='/data1/sap/interpark_data/test/label_Corntea_Kantata.txt'
names_file = '/home/sap/darknet_interpark/Corntea_Kantata/obj.names'
'''
detection_file = '/home/sap/darknet_interpark/Corntea_Kantata_600_org/classification_result/Corntea_Kantata_600_org_4000.log'
gt_file ='/data1/sap/interpark_data/test/label_Corntea_Kantata.txt'
names_file = '/home/sap/darknet_interpark/Corntea_Kantata_600_org/obj.names'


names_list = get_list_from_file(names_file)
names_size = len(names_list) + 1
TP_list = [0] * names_size
FP_list = [0] * names_size
FN_list = [0] * names_size

cm_truth = list()
cm_pred = list()
bg = names_size -1
double_box = names_size

label_lines = get_list_from_file(gt_file)
detection_lines = get_list_from_file(detection_file)

for label_line, detection_line in zip(label_lines, detection_lines) :
    label_line_split = label_line.split()
    truth_file_name = label_line_split[0]
    if(len(label_line_split) == 1) :
        truth_class = bg
    else :
        truth_class = int(label_line_split[1])

    detection_line_split = detection_line.split()
    detection_file_name = detection_line_split[0]
    if(truth_file_name !=detection_file_name):
        print(truth_file_name, "!=", detection_file_name)
        sys.exit(1)
    detection_classes = detection_line_split[1:]
    
    is_found = 0
    for detection_class in detection_classes :
        cm_truth.append(truth_class)
        detection_class = int(detection_class)
        if truth_class == detection_class :
            if is_found :
                FP_list[truth_class]+=1
                cm_pred.append(double_box)
            else :
                TP_list[truth_class]+=1
                cm_pred.append(truth_class)
                is_found = 1
        else :
            FP_list[detection_class]+=1
            cm_pred.append(detection_class)
    if not is_found :
        FN_list[truth_class]+=1
        cm_truth.append(truth_class)
        cm_pred.append(bg)

precision_list = [0.] * (names_size -1)
recall_list = [0.] * (names_size - 1)

for class_num, (TP, FP, FN) in enumerate(zip(TP_list[:-1], FP_list[:-1], FN_list[:-1])) :
    if FN+TP == 0 or FP+TP == 0 : continue
    precision = round(TP / float(TP + FP ), 3)
    recall = round(TP / float(TP + FN ), 3)
    precision_list[class_num] = precision
    recall_list[class_num] = recall 

#result_file = open(result_file_path, 'w')
#result_file.write("name\tprecision\trecall\n")
print("name\tprecision\trecall")
for name, precision, recall in zip(names_list, precision_list, recall_list) :
    buff = name + "\t" + str(precision) + "\t" + str(recall)
#    result_file.write(buff+"\n")
    print(buff)
#result_file.close()

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels

def plot_confusion_matrix(y_true, y_pred, classes,
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
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
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
           xticklabels=classes, yticklabels=classes,
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

class_names = np.array(names_list)
class_names = np.append(class_names, ["bg", "double box"])
print(confusion_matrix(cm_truth, cm_pred))
plot_confusion_matrix(cm_truth, cm_pred, class_names)

plt.rcParams["figure.figsize"] = (500, 500)
#plt.figure(figsize= (50, 50))
plt.savefig('test.png')
plt.show()

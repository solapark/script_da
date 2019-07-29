from utils import *
import sys

'''
label_file ='/data1/sap/interpark_data/test/label.txt'
detection_file ='/home/sap/darknet_interpark/181210_test/classfication_result/base_120000_thresh_80.log'
result_file_path ='/home/sap/darknet_interpark/181210_test/map/base_120000_thresh_80.log'
names_file ='/home/sap/darknet_interpark/181210_test/obj.names' 
'''
label_file ='/data1/sap/interpark_data/test/label_bad_obj6.txt'
detection_file = '/home/sap/darknet_interpark/bad_obj6/classification_result/bad_obj6_12000.log'
result_file_path ='/home/sap/darknet_interpark/bad_obj6/map/bad_obj6_12000.log'
names_file = '/home/sap/darknet_interpark/bad_obj6/obj.names'

names_list = get_list_from_file(names_file)
names_size = len(names_list) + 1
TP_list = [0] * names_size
FP_list = [0] * names_size
FN_list = [0] * names_size

label_lines = get_list_from_file(label_file)
detection_lines = get_list_from_file(detection_file)

for label_line, detection_line in zip(label_lines, detection_lines) :
    label_line_split = label_line.split()
    truth_file_name = label_line_split[0]
    if(len(label_line_split) == 1) :
        truth_class = -1
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
        detection_class = int(detection_class)
        if truth_class == detection_class :
            if is_found :
                #FP_list[truth_class]+=1
                is_found = 1
            else :
                is_found = 1
                TP_list[truth_class]+=1
        else :
            FP_list[detection_class]+=1
    if not is_found :
        FN_list[truth_class]+=1

precision_list = [0.] * (names_size -1)
recall_list = [0.] * (names_size - 1)

for class_num, (TP, FP, FN) in enumerate(zip(TP_list[:-1], FP_list[:-1], FN_list[:-1])) :
    if FN+TP == 0 or FP+TP == 0 : continue
    precision = round(TP / float(TP + FP ), 3)
    recall = round(TP / float(TP + FN ), 3)
    precision_list[class_num] = precision
    recall_list[class_num] = recall 

result_file = open(result_file_path, 'w')
result_file.write("name\tprecision\trecall\n")
print("name\tprecision\trecall")
for name, precision, recall in zip(names_list, precision_list, recall_list) :
    buff = name + "\t" + str(precision) + "\t" + str(recall)
    result_file.write(buff+"\n")
    print(buff)
result_file.close()

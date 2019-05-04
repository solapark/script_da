import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('cityscapes_8class', 'train'), ('cityscapes_8class', 'test'), ('synthia', 'train'), ('synthia', 'test')]
#classes = ["car"]
classes = ['person',	'rider',	'car',	'truck',	'bus',	'train',	'motorcycle',	'bicycle']


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_file, txt_file):
    in_file = open(xml_file)
    out_file = open(txt_file, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd ='/home/sap/dataset/xml_labels'
img_dir = '/home/sap/dataset/images'

for data_name, kind in sets:
    path =wd +'/'+data_name+ '/'+kind  
    if not os.path.exists(path):
        print ('theres no path %s' %(path))

    xml_files = os.listdir(path)
    list_file_name =img_dir+'/'+data_name+'/' + data_name + '_' + kind + '.txt' 

    list_file = open(list_file_name, 'w')

    for xml_file in xml_files:
        image_file = img_dir + '/'+data_name + '/'+kind + '/'+xml_file.replace(".xml", ".jpg")
        txt_file = image_file.replace(".jpg", ".txt")
        xml_file = wd + '/' + data_name +'/'+ kind +'/'+ xml_file

        convert_annotation(xml_file, txt_file)
        list_file.write('%s\n' %(image_file))

    list_file.close()
    print('%s %s DONE' %(data_name, kind))

#os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
#os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")


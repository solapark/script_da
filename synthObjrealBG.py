from PIL import Image
import math
import random
import cv2
import copy
import numpy as np

'''
input = real image path, synth image path, synth seg path
output = real bg + synth obj image

function 1 : real image size = synth image size
function 2 : copy mask of synth obj -> paste to real
'''
def tile_image(src, target, direction):
    if(direction == 'width'):
        num_of_tile =  math.ceil(target.shape[1]/src.shape[1])
        src_width = src.shape[1]
        result_width = num_of_tile * src.shape[1]
        result = np.zeros((src.shape[0],result_width, 3), np.uint8)
        for i in range(num_of_tile) :
            offset = i*src.shape[1]
            result[0:, offset:offset+src_width] = src

    elif(direction == 'height'):
        num_of_tile =  math.ceil(target.shape[0]/src.shape[0])
        src_height = src.shape[0]
        result_height = num_of_tile * src.shape[0]
        result = np.zeros((result_height ,src.shape[1],3), np.uint8)
        for i in range(num_of_tile):
            offset = i*src.shape[0]
            result[offset:offset+src_height,0:] = src
    return result

def random_crop(src, target):
    crop_width, crop_height = target.shape[1], target.shape[0] 
    x = random.randint(0, src.shape[1] -crop_width) 
    y = random.randint(0, src.shape[0]-crop_height)
    croped_src = src[y:y+crop_height, x:x+crop_width]

    return croped_src 

def src2target_size (src, target):
    if (src.shape[1] < target.shape[1]) :
        src = tile_image(src, target, 'width')
    if (src.shape[0] < target.shape[0]):
        src = tile_image(src, target, 'height')
    if (src.shape[1] > target.shape[1]) or (src.shape[0] > target.shape[0]):
        src = random_crop(src, target)

    return src 

def make_real_bg_synth_obj(real_image, synth_image, synth_seg):
    synth_sized_real= src2target_size(real_image, synth_image)
    gray_synth_seg = cv2.cvtColor(synth_seg, cv2.COLOR_BGR2GRAY)
    _, binary_synth_seg = cv2.threshold(gray_synth_seg, 0, 255, cv2.THRESH_BINARY)
    binary_synth_seg_inv = cv2.bitwise_not(binary_synth_seg)

    real_bg = cv2.bitwise_and(synth_sized_real, synth_sized_real, mask = binary_synth_seg_inv)
    synth_obj = cv2.bitwise_and(synth_image, synth_image, mask = binary_synth_seg)

    real_bg_synth_obj = cv2.add(real_bg, synth_obj) 

    return real_bg_synth_obj


def get_box_list_from_yolo_label(image_path, label_path):
    #return box_list [(x1, y1, x2, y2), .....]
    image = cv2.imread(image_path)
    image_width = image.shape[1]
    image_height = image.shape[0]

    label_file = open(label_path, 'r')
    lines = label_file.readlines()
    label_file.close()

    box_list = []

    for line in lines :
        token = line.split()
        relative_x_center = float(token[1])
        relative_y_center = float(token[2])
        relative_width = float(token[3])
        relative_height = float(token[4])

        absolute_x_center = relative_x_center * image_width
        absolute_y_center = relative_y_center * image_height
        absolute_width = relative_width * image_width
        absolute_height = relative_height * image_height

        left_x = round(absolute_x_center - absolute_width/2.0)
        right_x = round(absolute_x_center + absolute_width/2.0)
        top_y = round(absolute_y_center - absolute_height/2.0)
        bottom_y = round(absolute_y_center + absolute_height/2.0)
        box_width = round(absolute_width)
        box_height = round(absolute_height)

        box = {"left_x":left_x,"top_y": top_y, "right_x":right_x, "bottom_y":bottom_y, "width":box_width, "height":box_height}
        box_list.append(box)

    return box_list

def get_label_path_from_image_path(image_path):
    return image_path.replace(".jpg", ".txt")

def get_seg_path_from_image_path(image_path, seg_dir) :
    image_name = image_path.split('/')[-1]
    seg_name = image_name.replace("source_", "")
    seg_name = seg_name.replace(".jpg", ".png")

    seg_path = seg_dir + seg_name
    return seg_path

def get_save_path(synth_image_path, save_dir):
    image_name = synth_image_path.split('/')[-1]
    save_path = save_dir + image_name
    return save_path

def iou(boxA, boxB) :
    xA = max(boxA['left_x'], boxB['left_x'])
    yA = max(boxA['top_y'], boxB['top_y'])
    xB = min(boxA['right_x'], boxB['right_x'])
    yB = min(boxA['bottom_y'], boxB['bottom_y'])
 
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
    boxAArea = (boxA['right_x'] - boxA['left_x'] + 1) * (boxA['bottom_y'] - boxA['top_y'] + 1)
    boxBArea = (boxB['right_x'] - boxB['left_x'] + 1) * (boxB['bottom_y'] - boxB['top_y'] + 1)
 
    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou

def get_new_bg(image_path_list, my_box):
    random_image_path_list = copy.deepcopy(image_path_list)
    random.shuffle(random_image_path_list)
    for i, image_path in enumerate(random_image_path_list):
        label_path = get_label_path_from_image_path(image_path)
        cand_box_list = get_box_list_from_yolo_label(image_path,label_path) 
        is_find_target_bg = 1
        for cand_box in cand_box_list :
            if iou(cand_box, my_box) :
                is_find_target_bg = 0
                break;

        if(is_find_target_bg) : 
            target_bg = cv2.imread(image_path)
            return target_bg


    print("no pure bg")
    image = cv2.imread(image_path_list[0])
    height, width = image.shape[:2] 
    left_x = random.randint(0, width-1)
    top_y = random.randint(0, height-1) 
    box_width =width / 10
    box_height = height / 10 
    right_x = left_x + box_width - 1
    bottom_y = top_y + box_height -1
    small_box = {"left_x":left_x,"top_y": top_y, "right_x":right_x, "bottom_y":bottom_y, "width":box_width, "height":box_height}
    
    target_bg = get_new_bg(image_path_list, small_box)          
    crop_bg = target_bg[small_box['top_y']:small_box['bottom_y'], small_box['left_x']:small_box['right_x']]
    new_bg = src2target_size(crop_bg, target_bg)
    return new_bg


def erase_object(image_path, label_path, image_path_list):
#    return image in which object is removed and the region of object is filled with other image's pure background
    image = cv2.imread(image_path)
    box_list = get_box_list_from_yolo_label(image_path, label_path)
    for box in box_list :
        new_bg = get_new_bg(image_path_list, box)
        new_bg_cropped = new_bg[box['top_y']:box['bottom_y'], box['left_x']:box['right_x']]
        image[box['top_y']:box['bottom_y'], box['left_x']:box['right_x']] = new_bg_cropped

    return image 
        
def draw_label(image_path, label_path) :
    image = cv2.imread(image_path)
    box_list = get_box_list_from_yolo_label(image_path, label_path)
    for box in box_list :
        left_top = (box['left_x'], box['top_y'])
        right_bottom = (box['right_x'], box['bottom_y'])
        cv2.rectangle(image, left_top, right_bottom, (0, 255, 0), 3)
        #cv2.rectangle(real_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 3)

    cv2.imshow('result', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def synthOBJ_realBG_excluding_realOBJ(real_image_path_list_file_path, synth_image_path_list_file_path, synth_seg_dir, save_dir) :
    real_image_path_list_file = open(real_image_path_list_file_path, 'r')
    real_image_path_list = real_image_path_list_file.read().splitlines()
    real_image_path_list = [real_image_path for real_image_path in real_image_path_list if real_image_path]
    real_image_path_list_file.close()

    real_size = len(real_image_path_list)
    object_erased_real_list = []

    for i, real_image_path in enumerate(real_image_path_list) :
        real_label_path = get_label_path_from_image_path(real_image_path)
        object_erased_real = erase_object(real_image_path, real_label_path, real_image_path_list)
        #cv2.imshow('object_erased_real',object_erased_real )
        #cv2.waitKey(0)
        object_erased_real_list.append(object_erased_real)
        if(i%10 == 0):
            print("erasing object in real image %s/%s done" %(i, real_size))
    

    synth_image_path_list_file = open(synth_image_path_list_file_path, 'r')
    synth_image_path_list = synth_image_path_list_file.read().splitlines()
    synth_image_path_list = [synth_image_path for synth_image_path in synth_image_path_list if real_image_path]
    synth_image_path_list_file.close()
    synth_size = len(synth_image_path_list)

    for i, synth_image_path in enumerate(synth_image_path_list) :
        synth_seg_path = get_seg_path_from_image_path(synth_image_path, synth_seg_dir)
        synth_image = cv2.imread(synth_image_path)
        synth_seg_image = cv2.imread(synth_seg_path)
        object_erased_real =object_erased_real_list[i%real_size] 

        real_bg_synth_obj = make_real_bg_synth_obj(object_erased_real, synth_image, synth_seg_image)
        save_path = get_save_path(synth_image_path, save_dir)
        cv2.imwrite(save_path, real_bg_synth_obj)
        if(i%50 == 0):
            print("synth obj + real bg %s/%s done" %(i, synth_size))
        #cv2.imshow('real_bg_synth_obj', real_bg_synth_obj)
        #cv2.waitKey(0)

    #cv2.destroyAllWindows()

if __name__ == "__main__":
    cityscapes_train_image = "/home/sap/dataset/images/cityscapes/cityscapes_train.txt"
    sim10k_train_image = "/home/sap/dataset/images/sim10k/sim10k_train.txt"
    sim10k_seg_dir = "/data1/sap/sim10k/segmentation/VOC2012/SegmentationObject/"
    sim10kOBJ_cityscapesBG_train = "/home/sap/dataset/images/sim10kOBJ_cityscapesBG_excluding_cityscapesOBJ/train/"

    sim10k_test_image = "/home/sap/dataset/images/sim10k/sim10k_test.txt"
    sim10kOBJ_cityscapesBG_test = "/home/sap/dataset/images/sim10kOBJ_cityscapesBG_excluding_cityscapesOBJ/test/"

    synthOBJ_realBG_excluding_realOBJ(cityscapes_train_image, sim10k_train_image, sim10k_seg_dir, sim10kOBJ_cityscapesBG_train)
    synthOBJ_realBG_excluding_realOBJ(cityscapes_train_image, sim10k_test_image, sim10k_seg_dir, sim10kOBJ_cityscapesBG_test)
'''
    real_image_path_list_file = open(real_image_path_list_file_path, 'r')
    real_image_path_list = real_image_path_list_file.read().splitlines()
    real_image_path_list_file.close()

    real_size = len(real_image_path_list)
    object_erased_real_list = []

    for i, real_image_path in enumerate(real_image_path_list) :
        real_label_path = get_label_path_from_image_path(real_image_path)
        object_erased_real = erase_object(real_image_path, real_label_path, real_image_path_list)
        #cv2.imshow('object_erased_real',object_erased_real )
        #cv2.waitKey(0)
        object_erased_real_list.append(object_erased_real)
        if(i%10 == 0):
            print("erasing object in real image %s/%s done" %(i, real_size))
    

    synth_image_path_list_file = open(synth_image_path_list_file_path, 'r')
    synth_image_path_list = synth_image_path_list_file.read().splitlines()
    synth_image_path_list_file.close()

    for i, synth_image_path in enumerate(synth_image_path_list) :
        synth_seg_path = get_seg_path_from_image_path(synth_image_path, synth_seg_dir)
        synth_image = cv2.imread(synth_image_path)
        synth_seg_image = cv2.imread(synth_seg_path)
        object_erased_real =object_erased_real_list[i%real_size] 

        real_bg_synth_obj = make_real_bg_synth_obj(object_erased_real, synth_image, synth_seg_image)
        cv2.imshow('real_bg_synth_obj', real_bg_synth_obj)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
'''

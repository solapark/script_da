from synthObjrealBG import *
import cv2

def get_path_list_from_file(file_path):
    path_list_file = open(file_path, 'r')
    path_list = path_list_file.read().splitlines()
    path_list = [path for path in path_list if path]
    path_list_file.close()

    return path_list 

def get_new_image_path_from_image_path(image_path, new_image_dir) :
    image_name = image_path.split('/')[-1]
    new_image_path = new_image_dir + image_name
    return new_image_path

def erase_vague_obj(image_path_list_file_path):
    image_path_list =get_path_list_from_file(image_path_list_file_path)
    image_len = len(image_path_list)

    for i, image_path in enumerate(image_path_list) :
        label_path = get_label_path_from_image_path(image_path)
        object_erased_image = erase_object(image_path, label_path, image_path_list)
        cv2.imwrite(image_path, object_erased_image)
        #cv2.imshow('removed', object_erased_image)
        #cv2.waitKey(1)
        print(image_path)
        if(i%10 == 0):
            print("erasing object %s / %s done" %(i+1, image_len))

def revive_object(removed_obj_path, label_path, raw_image_path) :
    raw_image = cv2.imread(raw_image_path)
    removed_obj_image = cv2.imread(removed_obj_path)
    box_list = get_box_list_from_yolo_label(raw_image_path, label_path)
    for box in box_list :
        obj_cropped = raw_image[box['top_y']:box['bottom_y'], box['left_x']:box['right_x']]
        removed_obj_image[box['top_y']:box['bottom_y'], box['left_x']:box['right_x']] = obj_cropped

    return removed_obj_image 

def revive_real_obj(image_path_list_file_path, removed_obj_dir, raw_image_dir):
    image_path_list =get_path_list_from_file(image_path_list_file_path)
    image_len = len(image_path_list)

    for i, image_path in enumerate(image_path_list) :
        removed_obj_path =get_new_image_path_from_image_path(image_path, removed_obj_dir)
        raw_image_path = get_new_image_path_from_image_path(image_path, raw_image_dir)
        label_path = get_label_path_from_image_path(image_path)
        object_revived_image = revive_object(removed_obj_path, label_path, raw_image_path)
        cv2.imwrite(image_path, object_revived_image)
        print(image_path)
        #draw_label(image_path, label_path)
        #cv2.imshow(image_path, object_revived_image)
        #cv2.waitKey(0)
        if(i%10 == 0):
            print("reviving object %s / %s done" %(i+1, image_len))

if __name__ == "__main__":
    erase_target = '/home/sap/dataset/images/cityscapes_pseudo_label/cityscapes_pseudo_label_thresh_0.001.txt'
    erase_dir = '/home/sap/dataset/images/cityscapes_pseudo_label/thresh_0.001/'
    revive_target = '/home/sap/dataset/images/cityscapes_pseudo_label/cityscapes_pseudo_label_thresh_0.8.txt'
    raw_image_dir = '/home/sap/dataset/images/cityscapes/train/'
    #erase_vague_obj(erase_target)
    revive_real_obj(revive_target, erase_dir, raw_image_dir)

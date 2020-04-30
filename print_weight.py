import cv2

path = '/home/sap/darknet_interpark/activation_map/wgt/Layer_93.jpg'
anchor = 0
class_num = 0
anchor_size = 7

if __name__ == '__main__' :
    wgt = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    #idx = 7 * anchor + 5 + class_num
    #idx = anchor_size * anchor + 5 + class_num
    idx = anchor_size * anchor + 4 
    final = wgt[idx]
    for d in final :
        #print(d, end='\t')
        print(d)
    print() 

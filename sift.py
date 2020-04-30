'''
import numpy as np
import cv2
from matplotlib import pyplot as plt
 
#/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_0_1000.jpg
#/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_1_1000.jpg
#/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_2_1000.jpg
img1 = cv2.imread('/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_1_1001.jpg',0)
img2 = cv2.imread('/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_2_1001.jpg',0)
 
sift = cv2.xfeatures2d.SIFT_create()
 
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
 
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
 
good = []
for m,n in matches:
    if m.distance < .9*n.distance:
        good.append([m])
 
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
 
plt.imshow(img3),plt.show()
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img1 = cv2.imread('/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_1_1001.jpg',0)
img2 = cv2.imread('/data1/sap/interpark_data/train/extra_1210_mod/images/TunaCan_2_1001.jpg',0)
 
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
 
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
 
# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
 
flann = cv2.FlannBasedMatcher(index_params,search_params)
 
matches = flann.knnMatch(des1,des2,k=2)
 
# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]
 
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.3*n.distance:
        matchesMask[i]=[1,0]
 
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)
 
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
 
plt.imshow(img3,),plt.show()

#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# @Author: zxc


import cv2
import numpy as np
img=cv2.imread('./label.jpg',0)
#laplacian算子,使滤波后图像仍清晰
laplacian = cv2.Laplacian(img,cv2.CV_64F)
#高斯平滑滤波消除噪音
img_gass = cv2.GaussianBlur(laplacian,(5,5),0)
#二值化
ret1,img_BINARY=cv2.threshold(img_gass,3,255,cv2.THRESH_BINARY)
img_BINARY = cv2.resize(img_BINARY,(700,500))
cv2.imshow('ttt',img_BINARY)
cv2.waitKey(0)
cv2.destroyAllWindows()
#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# @Author: zxc

import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('./girl.png',0)
#统计直方图
#hist为256x1的数组
# hist = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.hist(img.ravel(),256,[0,256])
# #绘制直方图
# plt.show()
# equ = cv2.equalizeHist(img)
# res = np.hstack((img,equ))
#适应性直方图
clahe = cv2.createCLAHE(clipLimit=8.0,tileGridSize=(4,4))
cl1 = clahe.apply(img)
# cv2.imwrite('res.png',res)
cv2.imshow('cl1',cl1)
# cv2.imwrite('cl1.png',cl1)
img_c = cv2.imread('./girl.png')
#先转化为HSV图像
hsv = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
#H,S 2D直方图
hist = cv2.calcHist([hsv],[0,1],None,[180,256],[0,180,0,256])
plt.imshow(hist,interpolation='nearest')
plt.show()
cv2.waitKey(0)
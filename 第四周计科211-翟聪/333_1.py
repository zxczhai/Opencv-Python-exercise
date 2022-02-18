#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# @Author: zxc

import cv2
import numpy as np
import math
img = cv2.imread('./gun.jpg',cv2.IMREAD_COLOR)
#重设大小便于观察
img = cv2.resize(img,(500,600))
#滤波处噪音
img_gs = cv2.GaussianBlur(img,(5,5),0)
#转化为hsv图像v
hsv = cv2.cvtColor(img_gs,cv2.COLOR_BGR2HSV)
#设定hsv范围
lower_hsv = np.array([0,80,46])
high_hsv = np.array([10,255,255])
img_range = cv2.inRange(hsv.copy(),lower_hsv,high_hsv)
img_range,contours,hierarchy = cv2.findContours(img_range,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
if len(contours)>0:
    #找出面积的最大轮廓
    c = max(contours,key=cv2.contourArea)
    #使用最小外接圆圈出轮廓
    ((x,y),radius) = cv2.minEnclosingCircle(c)
    #计算轮廓的矩
    M = cv2.moments(c)
    #计算轮廓的重心
    center = (int(M['m10'] / M['m00']),int(M['m01'] / M['m00']))
    #画出最小外接圆
    cv2.circle(img, (int(x), int(y)), int(radius), (0, 0, 255), 3)
    #画出重心
    cv2.circle(img,center,5,(0,0,255),-1)
    #获取矩形参数
    ix,iy,iw,ih = cv2.boundingRect(c)
    min_rect = cv2.minAreaRect(c)
    # min_rect = ((min_rect[0][0],min_rect[0][1],min_rect[1][0],min_rect[1][1]),0)
    box = cv2.boxPoints(min_rect)
    box = np.int0(box)
    #输出矩形
    cv2.drawContours(img,[box],0,(0,255,0),3)
    #输出矩形的中心
    # rect_radius = int(math.sqrt((0.5*min_rect[1][0])**2+(0.5*min_rect[1][1])**2))
    cv2.circle(img,(int((min_rect[0])[0]),int((min_rect[0])[1])),5,(0,255,0),-1)
    cv2.imshow('ok',img)
    cv2.imshow('ttt',img_range)
print("圆形中心点:")
print(int(x),int(y),'\n')
print("矩形长宽:")
print(min_rect[1][0],min_rect[1][1])
print("圆形半径:")
print(radius)
print("四个极点")
leftmost = tuple(c[c[:,:,0].argmin()][0])
rightmost = tuple(c[c[:,:,0].argmax()][0])
topmost = tuple(c[c[:,:,1].argmin()][0])
bottommost = tuple(c[c[:,:,1].argmax()][0])
print(leftmost,rightmost,topmost,bottommost)
cv2.waitKey(0)
cv2.destroyAllWindows()
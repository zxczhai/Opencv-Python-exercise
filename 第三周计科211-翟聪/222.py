#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# @Author: zxc
import cv2
import numpy as np
def nothing(x):
    pass
img=cv2.imread("./football.png")
#print (img.shape,'\n',img.size,'\n',img.dtype)
img1=cv2.imread("./cat.png")
img1=cv2.resize(img1,(750,467))
cv2.namedWindow('image')
cv2.createTrackbar('percent','image',0,100,nothing)
ball=img[380:470,450:540]
cv2.rectangle(ball,(0,0),(90,90),(0,0,255),2)
img[380:470,450:540]=ball
# print(th.shape)
# M=cv2.getRotationMatrix2D((cols/2,rows/2),-23,0.6)
# fin=cv2.warpAffine(th,M,(cols,rows))
while(1):
    percent = cv2.getTrackbarPos('percent', 'image')
    dst = cv2.addWeighted(img, percent/100, img1, 1 - (percent/100), 0)
    cv2.imshow('image',dst)
    k = cv2.waitKey(1) & 0xFF
    if k==27:
        break

img2=cv2.imread("./source/red block.png")
img2=cv2.resize(img2,(500,500))
img2_hsv=cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
#设置蓝色阈值(可向cv2.cvtColor()传入rgb值获取对应hsv值)
lower_red=np.array([20,100,100])
high_red=np.array([255,255,255])
#据阈值构建掩模
mask=cv2.inRange(img2_hsv,lower_red,high_red)

#(5,5)高斯核,o为标准差
blur = cv2.GaussianBlur(mask,(5,5),0)
ret,th=cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#将原图像和掩模进行位运算
th=cv2.bitwise_and(img2,img2,mask=th)
rows,cols,tmp=th.shape
pst1=np.float32([[154,210],[250,163],[170,286],[268,241]])
pst2=np.float32([[154,210],[400,210],[145,330],[400,330]])
M=cv2.getPerspectiveTransform(pst1,pst2)
fin=cv2.warpPerspective(th,M,(cols,rows))
cv2.imshow('th',fin)
cv2.waitKey(0)
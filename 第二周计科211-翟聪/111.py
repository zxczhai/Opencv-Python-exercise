#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# Author: zxc
import cv2
import numpy as np
import time
def nothing(x):
    pass
#when mouse down it turn True
drawing = False
#mode 判断
mode = 0

#判断左键或右键按下,从而使用矩形或圆形函数
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,b,g,r,img
    tmp=img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
    elif flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing ==True:
            if mode == 1:
                cv2.rectangle(img,(ix,iy),(x,y),(b,g,r),-1)
            elif mode == 2:
                cv2.rectangle(tmp,(ix,iy),(x,y),(b,g,r),2)
                cv2.imshow('image',tmp)
    elif event == cv2.EVENT_LBUTTONUP and mode ==2:
        cv2.rectangle(img, (ix, iy), (x, y), (b, g, r), 2)
    elif event == cv2.EVENT_RBUTTONDOWN:
        drawing = True
        ix,iy=x,y
    elif event==cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_RBUTTON:
        if drawing ==True:
            r1 = int(np.sqrt((x - ix) ** 2 + (y - iy) ** 2))
            cv2.circle(img,(ix,iy),r1,(b,g,r),-1)        #圆心不动,鼠标表示圆边界
    elif  event == cv2.EVENT_RBUTTONUP:
        drawing = False


#创建图像
img=np.zeros((512,512,3),np.uint8)
img[:]=[255,255,255]        #白色画布
cv2.namedWindow("image")
cv2.setMouseCallback('image',draw_circle)
#滑动条调节颜色
cv2.createTrackbar("R","image",0,255,nothing)
cv2.createTrackbar("G","image",0,255,nothing)
cv2.createTrackbar("B","image",0,255,nothing)
while(1):
    k=cv2.waitKey(1)&0xFF
    cv2.imshow("image", img)
    if k==27:
        break
    elif k == ord('1'):
        mode = 1
    elif k == ord('2'):
        mode = 2
#滑动条与窗口绑定
    r=cv2.getTrackbarPos('R','image')
    g=cv2.getTrackbarPos('G','image')
    b=cv2.getTrackbarPos('B','image')
cv2.destroyAllWindows()
exit(0)
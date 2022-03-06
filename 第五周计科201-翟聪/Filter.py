#!U:\Python3.6.7
# - *- coding:utf-8 -*-
# @Author: zxc

import cv2
import numpy as np
from matplotlib import pyplot as plt
#应用DFT
img = cv2.imread('house.jpg',0)
dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
#构建振幅图
magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
rows,cols = img.shape
crow,ccol = rows/2,cols/2
#创建掩模
mask = np.zeros((rows,cols,2),np.uint8)
mask[int(crow-15):int(crow+15),int(ccol-15):int(ccol+15)] = 1
#应用掩模和逆DFT
fshift = dft_shift*mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
#绘制图像部分
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Input Image'),plt.xticks([]),plt.yticks([])
plt.subplot(122),plt.imshow(img_back,cmap = 'gray')
plt.title('Magnitude Spectrum'),plt.xticks([]),plt.yticks([])
plt.show()
cv2.imwrite('Filter.jpg',img_back)


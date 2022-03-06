### 第五周视觉任务 ###
#### 1. 直方图 ####
##### 代码思路 #####
读取一张灰度图,可直接使用equalizeHist()进行均衡化,也可使用cv2.createCLAHE()适应性直方图均衡化可防止对比度失衡.画2d直方图需先将彩色图像转化为HSV图像,使用calHist()即可.
详细代码如下:
```python
import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('./girl.png',0)
#适应性直方图
clahe = cv2.createCLAHE(clipLimit=8.0,tileGridSize=(4,4))
cl1 = clahe.apply(img)
# cv2.imwrite('res.png',res)
cv2.imshow('cl1',cl1)
# cv2.imwrite('cl1.png',cl1)
img_c = cv2.imread('./girl.png')
hsv = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
hist = cv2.calcHist([hsv],[0,1],None,[180,256],[0,180,0,256])
plt.imshow(hist,interpolation='nearest')
plt.show()
```

<img src="https://s3.bmp.ovh/imgs/2022/02/3a17e3ca81f11629.png" style="zoom: 50%;" />

<img src="https://i.bmp.ovh/imgs/2022/02/d93fe017303ee56f.png" style="zoom: 67%;" />


#### 2. 频率域滤波 ####
##### 代码思路 #####
首先使用快速傅里叶变换,使用高斯滤波等方式去除低频分量,再使用DFT的逆变换重建图像,从而去除图像中的竖条纹.
代码如下:
```python
import cv2
import numpy as np
from matplotlib import pyplot as plt
#应用DFT
img = cv2.imread('house.jpg',0)
dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
#构建振幅图
#magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
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
```

<img src="https://i.bmp.ovh/imgs/2022/02/61d7c09cc5de97e9.png" style="zoom:50%;" />
<img src="https://i.bmp.ovh/imgs/2022/02/685e9eb4f8e03030.png" style="zoom:50%;" />

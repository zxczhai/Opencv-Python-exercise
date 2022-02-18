### 第四周视觉任务 ###
1. 实现对标签图片进行处理,使标签文字以白色的形式显示清除
2. 实现用矩形和圆形识别饮料并输出各自的中心点,矩形的长宽,圆形半径,得到的四个极点
#### 具体代码如下 ####
1. 预处理标签
```python
#laplacian算子,使滤波后图像仍清晰
laplacian = cv2.Laplacian(img,cv2.CV_64F)
#高斯平滑滤波消除噪音
img_gass = cv2.GaussianBlur(laplacian,(5,5),0)
#二值化
ret1,img_BINARY=cv2.threshold(img_gass,3,255,cv2.THRESH_BINARY)
img_BINARY = cv2.resize(img_BINARY,(700,500))
```
2. 框定和圈定易拉罐
```python
#滤波除噪音
img_gs = cv2.GaussianBlur(img,(5,5),0)
#转化为hsv图像
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
```
##### 实现效果如下 #####
1. <img src = https://s2.loli.net/2021/12/23/DdEMU4gK9IcXhxG.png width = 50%/>
2. <img src =https://s2.loli.net/2021/12/23/QkOADqIvxu9bWa7.png width =50%/>
3. <img src = https://s2.loli.net/2021/12/23/SEOp7ibjQtwU2K5.png width = 50%/>
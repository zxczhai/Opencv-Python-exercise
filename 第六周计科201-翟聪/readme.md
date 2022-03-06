### 第六周视觉任务 ###
#### 霍夫线变化及模板匹配 ####
代码思路:
1.霍夫线变化,首先对图像进行边缘检测的处理,再通过函数HoughLines来实现.
2.模板匹配,首先确认模板,使用matchTemplate函数来实现.
##### 具体代码如下 #####
1.检测直线:
```python
img_rgb = cv2.imread('./checkerboard .png')
img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
#使用canny边缘检测显示直线
edges = cv2.Canny(img_gray,50,150,apertureSize=3)
#设置识别精确度和范围
lines = cv2.HoughLines(edges,1,np.pi/180,200)
for i in range(0,len(lines)):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*a)
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*a)
        #draw
        cv2.line(img_rgb,(x1,y1),(x2,y2),(0,255,0),2)
```
2.模板匹配
```python
#导入黑棋白棋模板(import　as gray)
template1 = cv2.imread('black.png',0)
template2 = cv2.imread('white.png',0)
#获得模板尺寸
w1,h1 = template1.shape[::-1]
w2,h2 = template2.shape[::-1]
#进行模板匹配
res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
#设置阈值
threshold = 0.8
loc_black = np.where(res1 >= threshold)
loc_white = np.where(res2 >= threshold)
#寻找多单位最远距离
#loc为符合条件的元组,img_rgb为绘制图像的彩色形式
def farest(loc,img_rgb):
    max = 0
    for pt in zip(*loc[::-1]):
        # cv2.rectangle(img_rgb,pt,(pt[0] + w1,pt[1] +h1),(0,0,255),1)
        last_bx = pt[0] + w1 / 2.0
        last_by = pt[1] + h1 / 2.0
        for npt in zip(*loc[::-1]):
            new_bx = npt[0] + w1 / 2.0
            new_by = npt[1] + h1 / 2.0
            # 计算两个棋子之间的距离
            bx_dis = abs(last_bx - new_bx)
            by_dis = abs(last_by - new_by)
            b_dis = math.sqrt(math.pow(bx_dis, 2) + math.pow(by_dis, 2))
            #找出距离最远的两个棋子
            if max < b_dis:
                max = b_dis
                point1 = (int(last_bx), int(last_by))
                point2 = (int(new_bx), int(new_by))
    cv2.line(img_rgb, point1, point2, (0, 0, 255), 2)
    print('ok')
#寻找相差最远的黑棋子
farest(loc_black,img_rgb)
#对白棋执行找最远棋子的操作
farest(loc_white,img_rgb)
cv2.imwrite('res1.png',img_rgb)
```
##### 效果如图 #####

![](https://s3.bmp.ovh/imgs/2022/02/9e400b38a4293150.png)
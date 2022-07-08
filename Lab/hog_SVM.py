import cv2
import numpy as np
import matplotlib.pyplot as plt

#1 训练 2 hog 3 svm 4 compute hog 5 label 6 train 7 predict 8 draw
#正样本数量
PosNum = 820
#负样本数量
NegNum = 1931
#窗体大小(样本分辨率64*128
winSize = (64,128)
#Block size
blockSize = (16,16) #105 个块
blockStride = (8,8) #4 cell
cellSize = (8,8)
nBin = 9 # 9 Bin 3780维

#2.create hog  1.win 2.block 3.blockStride   4.cell  5.bin
hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nBin)

#3.create svm
svm = cv2.ml.SVM_create()
#4.compute hog
featureNum = int(((128-16)/8+1)*((64-16)/8+1)*4*9)# 获取维度3780
featureArray  = np.zeros(((PosNum+NegNum),featureNum),np.float32)
labelArray = np.zeros(((PosNum+NegNum),1),np.int32)
#svm 监督学习
for i in range(0,PosNum):
    fileName = 'pos\\'+str(i+1)+'.jpg'
    img = cv2.imread(fileName)
    hist = hog.compute(img,(8,8))
    for j in range(0,featureNum):
        featureArray[i,j] = hist[j]
        # featureArray hog
        labelArray[i,0] = 1
        #正样本label 1
for i in range(0,NegNum):
    fileName = 'neg\\'+str(i+1)+'.jpg'
    img = cv2.imread(fileName)
    hist = hog.compute(img,(8,8))
    for j in range(0,featureNum):
        featureArray[i+PosNum,j]= hist[j]
        labelArray[i+PosNum,0] = -1
        #负样本label -1
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setC(0.01)
#6.train
ret = svm.train(featureArray,cv2.ml.ROW_SAMPLE,labelArray)

#7. test
alpha = np.zeros((1),np.float32)
rho = svm.getDecisionFunction(0,alpha)
print(rho)
print(alpha)
alphaArray = np.zeros((1,1),np.float32)
SVArray = np.zeros((1,featureNum),np.float32)#支持向量机数组
resArray  = np.zeros((1,featureNum),np.float32)
alphaArray[0,0] = alpha
resArray = -1*alphaArray*SVArray
#detect
myDetect = np.zeros((3781),np.float32)

for i in range(0,3780):
    myDetect[i] = resArray[0,i]
myDetect[3780] = rho[0]
#构建hog
myHog  = cv2.HOGDescriptor()
myHog.setSVMDetector(myDetect)
imageSrc  = cv2.imread('Test2.jpg',1)
object = myHog.detectMultiScale(imageSrc,0,(8,8),(32,32),1.05,2)
x = int(object[0][0][0])
y = int(object[0][0][1])
w = int(object[0][0][2])
h = int(object[0][0][3])
cv2.rectangle(imageSrc,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow("show",imageSrc)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2 as cv
import numpy as np
from numpy import bitwise_not

SZ=20
bin_n = 16 # Number of bins


affine_flags = cv.WARP_INVERSE_MAP|cv.INTER_LINEAR


## [deskew]去歪斜
def deskew(img):
    m = cv.moments(img)#获取图像的矩
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']#偏斜
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    # cv.imshow("deskew",img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return img
## [deskew]

## [hog] 定向梯度直方图
def hog(img):
    gx = cv.Sobel(img, cv.CV_32F, 1, 0)
    gy = cv.Sobel(img, cv.CV_32F, 0, 1)
    mag, ang = cv.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist
## [hog]

######     Now testing      ########################

svm = cv.ml.SVM_load("svm_data.dat")
cap  = cv.VideoCapture(0)
while(True):
    # ret,frame = cap.read()
    frame= cv.imread("4.jpg")
    img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    img  = cv.adaptiveThreshold(img_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    bitwise_not(img,img)
    deskewed = deskew(img)
    hogdata = hog(deskewed)
    testData = np.float32(hogdata).reshape(-1,bin_n*4)
    result = svm.predict(testData)[1].ravel()
    img = cv.resize(img,(480,640))
    cv.imshow("image",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    print(result)
    # print(result)
#######   Check Accuracy   ########################
# correct = np.count_nonzero(mask)
# print(correct*100.0/result.size)
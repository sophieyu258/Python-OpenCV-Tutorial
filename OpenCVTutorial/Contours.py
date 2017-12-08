import cv2
import numpy as np

dir = 'D:\\hbwork\\pyprojects\\data\\'

img = cv2.imread(dir + '17.png')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def Test1():    
    global img
    global imgray
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow('contours',img)
    #cnt = contours[0]
    #img = cv2.drawContours(img, [cnt], 0, (0,0,255), 3)

def Test2():
    global img
    global imgray
    ret, thresh = cv2.threshold(imgray, 127, 255,0)    
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[1]

    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        cv2.line(img,start,end,[0,255,0],2)
        cv2.circle(img,far,5,[0,0,255],-1)

    cv2.imshow('img',img)

if __name__ == "__main__":
    cv2.imshow('img',img)

    Test2()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
import numpy as np

dir = 'D:\\hbwork\\pyprojects\\data\\'

#img = cv2.imread(dir + 'messi5.jpg')
img = cv2.imread(dir + 'drawings.png')

def TestScaling():
    res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

    ##OR
    #height, width = img.shape[:2]
    #res = cv2.resize(img,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)
    return res

def TestTranslation():
    img = cv2.imread(dir + 'messi5.jpg',0)
    rows,cols = img.shape

    M = np.float32([[1,0,100],[0,1,50]])
    res = cv2.warpAffine(img,M,(cols,rows))

    return res

def TestRotation():
    img = cv2.imread(dir + 'messi5.jpg',0)
    rows,cols = img.shape

    M = cv2.getRotationMatrix2D((cols/2,rows/2),60,1)
    res = cv2.warpAffine(img,M,(cols,rows))

    return res

def TestAffine():    
    rows,cols,ch = img.shape

    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])

    M = cv2.getAffineTransform(pts1,pts2)

    res = cv2.warpAffine(img,M,(cols,rows))

    return res

def TestPerspective():
    rows,cols,ch = img.shape

    pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    res = cv2.warpPerspective(img,M,(300,300))

    return res

if __name__ == "__main__":

    dst = TestPerspective()

    cv2.imshow('original',img)
    cv2.imshow('transformed',dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
import numpy as np

print(cv2.__version__)

#cap = cv2.VideoCapture("C:\\opencv\\source_code\\opencv-3.3.0\\samples\\data\\vtest.avi")
cap = cv2.VideoCapture(0)   # capture from webcam

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

# cv2.imshow('frame1',frame1)

while(1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    # print(next.shape)

    cv2.imshow('prvs',prvs)
    cv2.imshow('next',next)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    #print(flow.shape)
    # print(flow.min())
    # print(flow.max())

    # print(flow[...,1].min())
    # print(flow[...,1].max())

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    #print(mag.shape)
    mag[mag == -np.inf] = 0
    print(mag.min())
    print(mag.max())
    hsv[...,0] = ang #*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('original',frame2)
    cv2.imshow('rgbflow',rgb)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',rgb)
    prvs = next

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
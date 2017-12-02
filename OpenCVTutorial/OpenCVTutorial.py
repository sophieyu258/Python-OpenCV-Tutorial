import numpy as np
import cv2
from matplotlib import pyplot as plt

dir = 'D:\\hbwork\\pyprojects\\data\\'

def Test1():
    # Load an color image in grayscale
    img = cv2.imread(dir + 'lena.jpg',cv2.IMREAD_COLOR)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',imggray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def Test2():
    img = cv2.imread(dir + 'lena.jpg',0)
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()

def Test3():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def Test4():
    cap = cv2.VideoCapture(dir + 'VID_20171105_110824.mp4')

    while(cap.isOpened()):
        try:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args

    cap.release()
    cv2.destroyAllWindows()

def Test5():
    cap = cv2.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)
            # write the flipped frame
            out.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    Test5()

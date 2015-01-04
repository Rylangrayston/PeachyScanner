import numpy as np
import cv2
import time as time






########## setup track ball window #############

def nothing(x):
    pass

def trackBallEvent(x):
    print(x, 'track ball has changed')

def setSaturation(x):
    satruationValue = x*.001
    print(x, satruationValue, 'track ball has changed')
    cap.set(11, satruationValue)

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)
cv2.createTrackbar('Saturation','image',0,1000,setSaturation)
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)
######################################################








def printCammeraSettings():
    x = [3,4,10,11,12,13,14]
    for ID in x:
        print(ID, "---->"  , cap.get(ID))





cap = cv2.VideoCapture(0)
cap.set(11, .5)



growingNumber = 0
while(True):
    growingNumber = 1 + growingNumber
    if growingNumber == 999:
        growingNumber = 0
############ run track ball window ################ 

    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    saturation = cv2.getTrackbarPos('Saturation','image')
    s = cv2.getTrackbarPos(switch,'image')

    cv2.setTrackbarPos('Saturation','image', growingNumber)

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
########################################################3




    #capture frame-by-frame
    
    ret, frame = cap.read()

    

# DISPLAY THE FRAME

    cv2.imshow('LiveFeedWindow', frame)
    #time.sleep(.2)
    #printCammeraSettings()



    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



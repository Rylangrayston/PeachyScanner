import numpy as np
import cv2
import time as time

def xyColorPicker(event,y,x,flags,param):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print ' mouse clicked at  x',  x, '   y',y
        #print frame[x,y][2]
        cv2.setTrackbarPos('R','image', frame[x,y][2])
        cv2.setTrackbarPos('G','image', frame[x,y][1])
        cv2.setTrackbarPos('B','image', frame[x,y][0])
        return([x,y])

    
    if event == cv2.EVENT_RBUTTONDOWN:
        global xPositionOfEncoderPixle, yPositionOfEncoderPixle
        xPositionOfEncoderPixle = x
        yPositionOfEncoderPixle = y


        return([x,y])
    



########## setup track ball window #############

def nothing(x):
    pass

def trackBallEvent(x):
    print(x, 'track ball has changed')

def setBrightness(x):
    brightness = x*.001
    print(x, brightness, 'track ball has changed')
    cap.set(10, brightness)


def setContrast(x):
    contrast = x*.001
    print(x, contrast, 'track ball has chaged contrast something')
    cap.set(11, contrast)

def setSaturation(x):
    saturation = x*.001
    print(x, saturation, 'track ball has changed saturation')
    cap.set(12, saturation)

def setHue(x):
    something = x*.001
    print(x, something, 'track ball has changed hue')
    cap.set(13, something)

def setGain(x):
    something = x*.001
    print(x, something, 'track ball has changed Gain')
    cap.set(14, something)

def setCenterOfRotation(x):
    global centerOfRotation, captureXResolution
    centerOfRotation = int(np.interp(x,[0,1000],[0,captureXResolution]))
    print(x, centerOfRotation, 'track ball has changed center of Rotation')
    

def setEncoderPixleValue(x):
    pass

def setSomething(x):
    something = x*.001
    print(x, something, 'track ball has something')
    cap.set(10, something)


# Create a black image, a window
img = np.zeros((100,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

cv2.createTrackbar('Brightness','image',0,1000,setBrightness)
cv2.createTrackbar('Contrast','image',0,1000,setContrast)
cv2.createTrackbar('Satruation','image',0,1000,setSaturation)
cv2.createTrackbar('Hue','image',0,1000,setHue)
cv2.createTrackbar('Gain','image',0,1000,setGain)
cv2.createTrackbar('Center Of Rotation','image',0,1000,setCenterOfRotation)
cv2.createTrackbar('Encoder Pixle Value','image',0,256*3 +5,setEncoderPixleValue)
cv2.createTrackbar('Encoder Pixle Debounce','image',0,1000,nothing)
cv2.createTrackbar('Encoder Pixle Lower Threshold','image',0,1000,nothing)
cv2.createTrackbar('Encoder Pixle Upper Threshold','image',0,1000,nothing)
cv2.createTrackbar('Number Of Encode Spots Detected','image',0,1000,nothing)
cv2.createTrackbar('something','image',0,1000,setSomething)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)
###############################################################################


def printCammeraSettings():
    x = [3,4,10,11,12,13,14] # 3 x res, 4 y res, 10 brightness, 11 contrast, 12 saturation, 13 hue, 14 gain
    for ID in x:
        print(ID, "---->"  , cap.get(ID))







cap = cv2.VideoCapture(0)
#cap.set(11, .5)

growingNumber = 500
firstLoop = True
cv2.namedWindow('LiveFeedWindow')
cv2.setMouseCallback('LiveFeedWindow',xyColorPicker)
centerOfRotation = 500
xPositionOfEncoderPixle = 100
yPositionOfEncoderPixle = 100
encodeSpotDark = True
numberOfEncodeSpotsDetected = 0

while(True):
   
    growingNumber = 1 + growingNumber
    if growingNumber == 999:
        growingNumber = 0


############ run track ball window ################ 

    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    

    # get current positions of all trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')

    brightness = cv2.getTrackbarPos('Brightness','image')
    contrast = cv2.getTrackbarPos('Contrast','image')
    saturation = cv2.getTrackbarPos('Saturation','image')
    hue = cv2.getTrackbarPos('Hue','image')
    gain = cv2.getTrackbarPos('Gain','image')
    centerOfRotation = cv2.getTrackbarPos('Center Of Rotation','image')
    #encoderPixleValue = cv2.getTrackbarPos('Encoder Pixle Value','image')
    encoderPixleDebounce = cv2.getTrackbarPos('Encoder Pixle Debounce','image')
    encoderPixleLowerThreshold = cv2.getTrackbarPos('Encoder Pixle Lower Threshold','image')
    encoderPixleUpperThreshold = cv2.getTrackbarPos('Encoder Pixle Upper Threshold','image')
    somthing = cv2.getTrackbarPos('somthing','image')
    
    s = cv2.getTrackbarPos(switch,'image')

    #cv2.setTrackbarPos('Brightness','image', growingNumber)
    

    
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
########################################################3




    #capture frame-by-frame
    
    ret, frame = cap.read()
    
    # Draw center Line:
    cv2.rectangle(frame,(centerOfRotation-2,5000),(centerOfRotation,0),(0,255,0),-1)
    # get value of encoder pixle
    encoderPixleValue = int(frame[xPositionOfEncoderPixle,yPositionOfEncoderPixle][0]) + int(frame[xPositionOfEncoderPixle,yPositionOfEncoderPixle][1]) + int(frame[xPositionOfEncoderPixle,yPositionOfEncoderPixle][2])  
    cv2.setTrackbarPos('Encoder Pixle Value','image', encoderPixleValue)
    
    #detect if there has been a new encoder spot detected:
    if encodeSpotDark and encoderPixleValue > encoderPixleUpperThreshold + encoderPixleDebounce:
        encodeSpotDark = False
        numberOfEncodeSpotsDetected += 1
        cv2.setTrackbarPos('Number Of Encode Spots Detected','image', numberOfEncodeSpotsDetected)
        

    if  not encodeSpotDark and encoderPixleValue < encoderPixleLowerThreshold - encoderPixleDebounce:
        encodeSpotDark = True
        #numberOfEncodeSpotsDetected += 1
        cv2.setTrackbarPos('Number Of Encode Spots Detected','image', numberOfEncodeSpotsDetected)
        

    
    

# DISPLAY THE FRAME

    cv2.imshow('LiveFeedWindow', frame)
    #time.sleep(.2)
    #printCammeraSettings()



    if cv2.waitKey(1) & 0xFF == 27:
        break

    
    if firstLoop:
        time.sleep(0)
        cv2.setTrackbarPos('Brightness','image', 500)
        cv2.setTrackbarPos('Contrast','image', 500)
        #cv2.setTrackbarPos('Saturation','image', 0) # why dose this cause a Segmentation Fault?
        cv2.setTrackbarPos('Hue','image', 500)
        cv2.setTrackbarPos('Gain','image', 500)
        cv2.setTrackbarPos('Encoder Pixle Debounce','image', 50)
        cv2.setTrackbarPos('Encoder Pixle Lower Threshold','image', 370)
        cv2.setTrackbarPos('Encoder Pixle Upper Threshold','image', 400)
        print 'first loop'
        captureXResolution = cap.get(3)
        captureYResolution = cap.get(4)

    if firstLoop:
        firstLoop = False

   # encoderPixleValue = 500
    

cap.release()
cv2.destroyAllWindows()



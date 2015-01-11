import numpy as np
import cv2
import cv
import time as time
import os
import math

def xyColorPicker(event,y,x,flags,param):  
    
    if event == cv2.EVENT_LBUTTONDOWN:  # gets the color under the mouse click
        print ' mouse clicked at  x',  x, '   y',y
        #print mat[x,y][2]
        cv2.setTrackbarPos('R','image', int(frame[x,y][2]))
        cv2.setTrackbarPos('G','image', int(frame[x,y][1]))
        cv2.setTrackbarPos('B','image', int(frame[x,y][0]))
        return([x,y])

    
    if event == cv2.EVENT_RBUTTONDOWN:  # gets the position under the mouse click
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
    #something = x*.001
    #print(x, something, 'track ball has something')
    #cap.set(10, something)
    pass


def changeCammera(x):
    global cap
    cap = cv2.VideoCapture(x)


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
cv2.createTrackbar('Use Cammera Number?','image',0,10,changeCammera)
cv2.createTrackbar('Contour Offset','image',0,40,nothing)

# create switch to turn on or off the data saving 
switch = '0 : toss data \n1 : Save .obj file'
cv2.createTrackbar(switch, 'image',0,1,nothing)  
###############################################################################


# prints out all the cammera setings i can get from a real time capture. 
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
saveRealTimeData = 0
firstSaveLoop = True  # we need to know if this is the first loop we will be saving data ... if it is we will reset all the loop counts 
newEncodeSpot = False
cv2.setTrackbarPos('Contour Offset','image',0)

###############################3
##############################
###############################


TEMP_IMAGE = '0000.jpg'  # dont think we need this right now
scan_method = 'spin'  #7
frameCount = 0 #7
pan = 0
#color to detect bgr
#R = 40
#G = 104
#B = 220
#amout grid size of points checked in image
skip_x = 2
skip_y = 2
skip_frame = 1
   
# factor scales the size of the object in output.obj
factor_y = .1
factor_x = .1
factor_z = .1

#string to hold all faces will be writen to obj file at the end of the scan
faces = ''

# is this the first frame? will be set to False after the first frame
first_frame = True

#how many rows were scanned in the first frame
rows_scaned = 0

# if the color of the detected pixle is difrenter than detect threshold is differnt from the goal color, we will move it far away from the modle making it easy to delete
detect_threshold = 150
# if the pixle is with in stop_looking_threshold then stop lookin for another one... this stops the scanner from detectign more than
#one line.
stop_looking_threshold = 100
first_row = True

current_row = 0

vert_index = 0

frames_per_revolution = 360
angle_step = math.pi * 2 / (frames_per_revolution / skip_frame)
angle = 0



# adds the differnce between 2 sets of 3 colors. Returns over all differnce which could be between 0 and (255 * 3) 
def color_dif(r,g,b,R,G,B):
    r_dif = abs(r - R)
    g_dif = abs(g - G)
    b_dif = abs(b - B)
    return(r_dif + g_dif + b_dif)

def exitScanner():
    if saveRealTimeData == 1:
        file.write(faces)
        print 'saving face'
    file.close()


file = open('output.obj', 'w')
# create an object in the .obj file
file.write('o PeachyScan\n')

###############################
###############################
############################







while(True):
   
    growingNumber = 1 + growingNumber
    if growingNumber == 999:
        growingNumber = 0


############ run track ball window ################ 

    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        exitScanner()
        break

    

    # get current positions of all trackbars
    R = cv2.getTrackbarPos('R','image')
    G = cv2.getTrackbarPos('G','image')
    B = cv2.getTrackbarPos('B','image')

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
    cameraNumber = cv2.getTrackbarPos('Use Cammera Number?','image')
    contourOffset = cv2.getTrackbarPos('Contour Offset','image') 
    
    saveRealTimeDataSwitch = cv2.getTrackbarPos(switch,'image')

    #cv2.setTrackbarPos('Brightness','image', growingNumber)
    

    # set the color of the color picker field :

    img[:] = [B,G,R]
########################################################3

    


    #capture frame-by-frame from image or live video
    
    ret, frame = cap.read()   #img = cv.QueryFrame(capture)  

    mat = cv.fromarray(frame, allowND=False)  # SHOULD NOT HAVE TO DO THIS ... we convert from numpy array to cvmat jsut and then back again.. simply because i havent coded it to wokr on numpy arraysyet ... 


    #cv2.imwrite('tmpIMAGE.png',frame)  

    #img = cv2.imread('tmpIMAGE.png',0)
    #print type(img)
    #time.sleep(3)

                  
    #cv.SaveImage(TEMP_IMAGE, frame)                                  ############# should NOT have to do this to get it to be the correct type cv matrix instead of np ary.... throws erorr saysing np.array has now atribute rows
    #mat = cv.LoadImageM(TEMP_IMAGE, cv.CV_LOAD_IMAGE_COLOR)   ###################################################################################

    # get value of encoder pixle
    encoderPixleValue = int(mat[xPositionOfEncoderPixle,yPositionOfEncoderPixle][0]) + int(mat[xPositionOfEncoderPixle,yPositionOfEncoderPixle][1]) + int(mat[xPositionOfEncoderPixle,yPositionOfEncoderPixle][2])  
    cv2.setTrackbarPos('Encoder Pixle Value','image', encoderPixleValue)    
   
    #detect if there has been a new encoder spot detected:
    newEncodeSpot = False
    if encodeSpotDark and encoderPixleValue > encoderPixleUpperThreshold + encoderPixleDebounce:
        encodeSpotDark = False
        numberOfEncodeSpotsDetected += 1
        newEncodeSpot = True
        cv2.setTrackbarPos('Number Of Encode Spots Detected','image', numberOfEncodeSpotsDetected)
    if  not encodeSpotDark and encoderPixleValue < encoderPixleLowerThreshold - encoderPixleDebounce:
        encodeSpotDark = True
        numberOfEncodeSpotsDetected += 1
        newEncodeSpot = True
        cv2.setTrackbarPos('Number Of Encode Spots Detected','image', numberOfEncodeSpotsDetected)
        

###################################################3
################   process a frame looking for laser light and save the data to an .obj file ##################################
##################################################
    
    first_row = True
    current_row = 0
    frameCount += 1
    if saveRealTimeDataSwitch == 1:
        saveRealTimeData = 1
        if firstSaveLoop:
            frameCount = 0
            rows_scaned = 0 
            first_row = True
            first_frame = True
            rows_scaned = 0
        firstSaveLoop = False
    if True and frameCount % skip_frame == 0:
                         
        print'prosesing frame ', frameCount 
        if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan':
            pan += .1
        if scan_method == 'spin':
            angle += angle_step
        for row_number in range(mat.rows):
            if row_number % skip_y == 0 :
                current_row += 1
                if first_frame and saveRealTimeData == 1:
                    rows_scaned += 1
                pixle_row = []

                for colum_number in range(mat.cols- contourOffset ):
                    if colum_number % skip_x == 0:
                        rgb = mat[row_number,colum_number]
                        b, g, r = rgb
                        color_dif(r,g,b,R,G,B)
                                 
                        pixle_row.append(color_dif(r,g,b,R,G,B))
                #print(max(pixle_row))
                       
                closest_yet = 20000
                position = 0
                bright_position = 0
                for pixle_value in pixle_row:
                    position += skip_x
                    if pixle_value < closest_yet:
                        closest_yet = pixle_value
                        bright_position = position
                        if pixle_value < stop_looking_threshold:
                            break
                #print(bright_position, ('*' * int(bright_position/20)) )

                if closest_yet < detect_threshold and bright_position > centerOfRotation:
                    if newEncodeSpot:
                         mat[row_number-skip_y, bright_position-skip_y + contourOffset] = (0,250,250)
                         
                    else:
                         mat[row_number-skip_y, bright_position-skip_y + contourOffset] = (0,250,0)
                    
                    if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan' and saveRealTimeData == 1 :
                        file.write('v ' + str(row_number * factor_y) + ' ' + str(bright_position * factor_x * math.cos(angle)) + ' ' + str(pan + (random.random()*.1)) + '\n')
                    if scan_method == 'spin' and saveRealTimeData == 1:
                        file.write('v ' + str(((bright_position - centerOfRotation) ) * math.cos(angle) ) + ' ' + str(row_number * factor_z)+ ' ' + str((bright_position -centerOfRotation ) * math.sin(angle) ) + '\n')
                        #print('spining')
                    do_face = True
                                
                else:
                    mat[row_number-skip_y, bright_position-skip_y + contourOffset] = (0,0,250)
                    if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan' and saveRealTimeData == 1 :
                        file.write('v ' + str(row_number * factor_y ) + ' ' + str(bright_position * factor_x) + ' ' + str(pan + (random.random()*.1)) + '\n')
                    if scan_method == 'spin' and saveRealTimeData == 1 :
                        file.write('v ' + str(((bright_position - centerOfRotation) ) * math.cos(angle) ) + ' ' + str(row_number * factor_z + 20 )+ ' ' + str((bright_position - centerOfRotation) * math.sin(angle) ) + '\n')
                            
                    do_face = False
                          
                if saveRealTimeData == 1:
                    vert_index += 1
                if not first_frame:
                    if first_row and do_face and saveRealTimeData == 1 :
                        face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - rows_scaned + 1) + '\n'
                        faces = faces + face

                    if not first_row and current_row != rows_scaned and do_face and saveRealTimeData == 1:
                        face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - rows_scaned + 1) + '\n'
                        faces = faces + face
                        face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - 1) + '\n'
                        faces = faces + face
                        #print(face,'..face')


            first_row = False
        first_frame = False


###################################################
#################################################33
#################################################3


    frame = np.asarray(mat) # GOING BACK TO ARRAY ... SO SLOW.. 

    # Draw center Line:
    cv2.rectangle(frame,(centerOfRotation-2,5000),(centerOfRotation,0),(0,255,0),-1)

 


    
    

# DISPLAY THE FRAME

    cv2.imshow('LiveFeedWindow', frame)

    #printCammeraSettings()



    if cv2.waitKey(1) & 0xFF == 27:
        exitScanner()
        break

    if newEncodeSpot:   # only for testing get rid of this soon!
        time.sleep(.3)

    
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



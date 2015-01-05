import numpy as np
import cv2

cap = cv2.VideoCapture(0)
x = [3,4,10,11,12,13,14]
cap.set(11, .5)
while(True):
    #capture frame-by-frame
    #cap.set(11, .8)
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# DISPLAY THE FRAME

    cv2.imshow('frame', frame)


    for ID in x:
        print(ID, "---->"  , cap.get(ID))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



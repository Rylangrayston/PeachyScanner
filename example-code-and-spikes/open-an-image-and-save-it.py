import numpy as np
import cv2

img = cv2.imread('yellow.png', 0,cv2.IMREAD_COLOR)
# print(img)

cv2.imshow('window-name', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.namedWindow('window-2', cv2.WINDOW_NORMAL)
cv2.imshow('window-2', img)
key = cv2.waitKey(0) & 0xFF

if key == 27:
    cv2.destroyAllWindows()

if key == ord('s'):
    cv2.imwrite('first-write.png',img)  
    print('file saved')
cv2.destroyAllWindows()



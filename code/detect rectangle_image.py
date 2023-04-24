import numpy as np
import cv2




#cap = cv2.VideoCapture(0)


img = cv2.imread('shapes1.png')
#gray = cv2.imread('shape.jpeg',0)


im = cv2.imread('test.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 10, 250)

# construct and apply a closing kernel to 'close' gaps between 'white'
# pixels
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)


im2, contours, hierarchy = cv2.findContours(closed.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print (len(contours))
#print (contours[0][2][0][0])
#print(contours[4][2])
ii = 0
jj = 0
x = 0
y = 0
x_ave = 0
y_ave = 0
while (ii < (len(contours))):

    #print (contours[ii][0])

    #print(len(contours[ii]))
    #print(ii)
    while (jj < len(contours[ii])):
        #print(contours[ii-1][jj-1])
        #print(contours[ii][jj][0])
        x = x + contours[ii][jj][0][0]
        y = y + contours[ii][jj][0][1]

        #print("ok")
        #print(ii, jj)
        jj = jj + 1

    x_ave = x / len(contours[ii])
    y_ave = y / len(contours[ii])
    #print(x_ave)
    jj = 0
    ii = ii + 1


cv2.drawContours(img, contours, -1, (0,255,0), 3)
#cv2.drawContours(img, contours, 0, (0,255,0), 3)

cv2.imshow("Image", img)
cv2.waitKey(0)
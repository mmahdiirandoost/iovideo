import numpy as np
import cv2

import time



#cap = cv2.VideoCapture(0)
print (time.time())

img = cv2.imread('shape.jpg')
#gray = cv2.imread('shape.jpeg',0)

#im = cv2.imread('test.jpg')
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
ii = 1
jj = 0
x = 0
y = 0
x_ave = 0
y_ave = 0
x2_ave = 0
y2_ave = 0
max_x = 0
min_x = 10000000000
max_y = 0
min_y = 10000000000
dir_x = 0
dir_y = 0

xxx = 0
yyy = 0

height2 = 0
width2 = 0

#print(contours)
#print(len(contours))
while (ii < (len(contours))):

    #print (contours[ii][0])

    #print(len(contours[ii]))
    #print(ii)

    while (jj < len(contours[ii])):
        #print(contours[ii-1][jj-1])
        #print(contours[ii][jj][0])


        #check circle


        if (contours[ii][jj][0][0] > max_x) :
            max_x = contours[ii][jj][0][0]

        if (contours[ii][jj][0][1] > max_y) :
            max_y = contours[ii][jj][0][1]

        if (contours[ii][jj][0][0] < min_x) :
            min_x = contours[ii][jj][0][0]

        if (contours[ii][jj][0][1] < min_y) :
            min_y = contours[ii][jj][0][1]


        x = x + contours[ii][jj][0][0]
        y = y + contours[ii][jj][0][1]




        #print("ok")
        #print(ii, jj)
        jj = jj + 1

    x_ave = x / len(contours[ii])
    y_ave = y / len(contours[ii])
    if (len(contours[ii]) > 30):
        xxx = (max_x + min_x) / 2
        yyy = (max_y + min_y) / 2
        print(xxx,yyy)




    width = max_x - min_x
    height = max_y - min_y

    #print (width,height,xxx,yyy)
    if (height > 2*width):

        height2 = y_ave
        width2 = x_ave



    elif (width > 2*height):
        height2 = y_ave
        width2 = x_ave
        print ("ok")



    max_x = 0
    max_y = 0
    min_x = 1000000000
    min_y = 1000000000
    x = 0
    y = 0
    jj = 0


    ii = ii + 1

    dir_x = xxx - width2
    dir_y = height2 - yyy
    print (dir_x , dir_y )
print (time.time())
cv2.drawContours(img, contours, -1, (0,255,0), 3)
#cv2.drawContours(img, contours, 0, (0,255,0), 3)


cv2.imshow("Image", img)
cv2.waitKey(0)
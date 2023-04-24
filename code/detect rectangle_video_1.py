import numpy as np
import cv2
import argparse


# badan bayad kamel konam
def create_hue_mask(image, lower_color, upper_color):
    lower = np.array(lower_color, np.uint8)
    upper = np.array(upper_color, np.uint8)

    # Create a mask from the colors
    mask = cv2.inRange(image, lower, upper)
    output_image = cv2.bitwise_and(image, image, mask=mask)
    return output_image


cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 10, 250)

    # construct and apply a closing kernel to 'close' gaps between 'white'
    # pixels
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    im2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)








    #im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    # print (len(contours))
    # print (contours[0][2][0][0])
    # print(contours[4][2])
    ii = 0
    jj = 0
    x = 0
    y = 0
    x_ave = 0
    y_ave = 0


    while (ii < (len(contours))):

        # print (contours[ii][0])

        # print(len(contours[ii]))
        # print(ii)
        while (jj < len(contours[ii])):
            # print(contours[ii-1][jj-1])
            # print(contours[ii][jj][0])
            x = x + contours[ii][jj][0][0]
            y = y + contours[ii][jj][0][1]

            # print("ok")
            # print(ii, jj)
            jj = jj + 1

        x_ave = x / len(contours[ii])
        y_ave = y / len(contours[ii])
        # print(x_ave)
        jj = 0
        ii = ii + 1
    cv2.drawContours(output, contours, -1, (0, 255, 0), 3)



    cv2.imshow('frame', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

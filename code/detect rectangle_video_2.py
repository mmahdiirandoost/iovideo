import numpy as np
import cv2
import argparse
from collections import deque

# badan bayad kamel konam
def create_hue_mask(image, lower_color, upper_color):
    lower = np.array(lower_color, np.uint8)
    upper = np.array(upper_color, np.uint8)

    # Create a mask from the colors
    mask = cv2.inRange(image, lower, upper)
    output_image = cv2.bitwise_and(image, image, mask=mask)
    return output_image
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])
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

    center = None

    # only proceed if at least one contour was found
    if len(contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(output, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(output, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines

        cv2.line(output, pts[i - 1], pts[i], (0, 0, 255), 1)



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

    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if the approximated contour has four points, then assume that the
        # contour is a book -- a book is a rectangle and thus has four vertices
        if len(approx) == 4:
            cv2.drawContours(output, [approx], -1, (0, 255, 0), 4)
            total += 1


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

 #   cv2.drawContours(output, contours, -1, (0, 255, 0), 3)



    cv2.imshow('frame', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

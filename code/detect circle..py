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
    frame = cv2.medianBlur(frame, 3)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Get lower red hue
    lower_red_hue = create_hue_mask(frame, [0, 100, 100], [10, 255, 255])
    # Get higher red hue
    higher_red_hue = create_hue_mask(frame, [160, 100, 100], [179, 255, 255])

    # detect Circle
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=60, param2=80, minRadius=0, maxRadius=0)
    # Display the resulting frame
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles


        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (255, 0, 0), 4)
            # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print(x, y, r)
    cv2.imshow('frame', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

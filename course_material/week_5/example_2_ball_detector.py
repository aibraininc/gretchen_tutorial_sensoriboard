
#!/usr/bin/env python
import numpy as np
import cv2
import imutils

# Class for detecting ball
class BallDetector:
    def __init__(self):
        # Lower limit for blue color
        self.colorLower = (20, 80, 80)
        # Upper limit for blue color
        self.colorUpper = ( 60, 255, 255)

    def detect(self, frame, _width):
        # 1. resize the frame, and convert it to the HSV
        frame = imutils.resize(frame, width= _width)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # 2. construct a mask for the color, then perform a series of dilations and erosions to remove any small
        # Use bilateralFilter for reducing unwanted noise
        hsv = cv2.bilateralFilter(hsv, 5, 175, 175)
        # Use inRange for getting specific color
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        # Erode and dilate image for isolation of individual elements and joining disparate elements in an image.
        mask = cv2.erode(mask, None, iterations=5)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.erode(mask, None, iterations=3)

        cv2.imshow("Filter", mask)

        # 3. find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        centor = None

        # 4. find the circles in the contours
        circles = []
        for cnt in cnts:
            # Calculate the the contourArea
            contour_area = cv2.contourArea(cnt)
            # Get the minEnclosingCicrle
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Calculate estimated radius and size of circle
            estimated_circle = 3.141592*radius*radius
            # Check the size of contour_area is similar to size of the circle
            similar = 1- abs(estimated_circle - contour_area)/estimated_circle
            if similar>0.75:
                circles.append(cnt)

        # 5. find the largest contour in the mask
        if len(circles) > 0:
            c = max(circles, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            centor = (int(x),int(y))
            # Only proceed if the radius meets a minimum size
            if radius > 10:
                # Draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, centor, 5, (0, 0, 255), -1)
        return [frame, centor]


#!/usr/bin/env python
import numpy as np
import cv2
import imutils

#class for detecting ball
class BallDetector:
    def __init__(self):

        #TODO: change lower limit and upper limit for hsv color that you want to detect
        self.colorLower = (90, 200, 80)
        self.colorUpper = (100, 255, 180)

    def detect(self, frame, _width = 640):
        # 1. resize the frame, and convert it to the HSV
        frame = imutils.resize(frame, width= _width)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # 2. construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("Filter", mask)

        # 3. find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        centor = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # 4. find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            centor = (int(x),int(y))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, centor, 5, (0, 0, 255), -1)
        return [frame, centor]

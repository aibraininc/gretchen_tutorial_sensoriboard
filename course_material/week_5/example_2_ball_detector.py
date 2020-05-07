
#!/usr/bin/env python
import numpy as np
import cv2
import imutils

#class for detecting ball
class BallDetector:
    def __init__(self):
        #lower limit for blue color
        self.colorLower = (20, 80, 80)
        #upper limit for blue color
        self.colorUpper = ( 60, 255, 255)

    def detect(self, frame, _width):
        # 1. resize the frame, and convert it to the HSV
        frame = imutils.resize(frame, width= _width)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        hsv = cv2.bilateralFilter(hsv, 5, 175, 175)
        # 2. construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
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
            contour_area = cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y,w,h),(0,255,0),2)
            estimated_r = ((w+h)/2.0)*0.5
            estimated_circle = 3.141592*estimated_r*estimated_r
            similar = 1- abs(contour_area - estimated_circle)/estimated_circle
            print(similar)
            if similar>0.75:
                circles.append(cnt)

        # 5. find the largest contour in the mask, then use
        if len(circles) > 0:
            c = max(circles, key=cv2.contourArea)
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

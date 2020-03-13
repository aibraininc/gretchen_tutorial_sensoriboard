
#!/usr/bin/env python
import numpy as np
import cv2
import imutils

class BallDetector:
    def __init__(self):
        self.greenLower = (29, 86, 6)
        self.greenUpper = (64, 255, 255)        


    def optimized(self,ball,frame):
        (image_height, image_width) = frame.shape[:2]

        target_offset_x = ball[0] - image_width / 2
        target_offset_y = ball[1] - image_height / 2
    
        try:
            percent_offset_x = float(target_offset_x) / (float(image_width) / 2.0)
            percent_offset_y = float(target_offset_y) / (float(image_height) / 2.0)
        except:
            percent_offset_x = 0
            percent_offset_y = 0
        return [percent_offset_x, percent_offset_y]


    def detect(self, frame, _width):
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width= _width)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        return (frame, center)

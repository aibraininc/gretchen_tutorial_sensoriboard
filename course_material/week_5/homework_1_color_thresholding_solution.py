#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

# Initalize camera
camera = Camera()
# Intalize point
point = (0,0)

# Lower limit for green color
colorLower = (20, 80, 80)
# Upper limit for green color
colorUpper = (60, 255, 255)

# Method called when clicked
def onMouse(event, u, v, flags, param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        img = camera.getImage()
        # Change image to hsv color space
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        point = (u,v)
        print('Point', u,v)
        # Print color RGB
        print('RGB', img[v,u])
        # Print color HSV
        print('HSV', hsv[v,u])

def color_filtering(frame):
    # 1. resize the frame, and convert it to the HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # 2. construct a mask for the color, then perform a series of dilations and erosions to remove any small
    # Use bilateralFilter for reducing unwanted noise
    hsv = cv2.bilateralFilter(hsv, 5, 175, 175)

    # Use inRange for getting specific color
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    # Erode and dilate image for isolation of individual elements and joining disparate elements in an image.
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=3)
    cv2.imshow("Filter", mask)

def main():
    global point
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
        # Draw circle on point
        cv2.circle(img, point, 10, (0, 0, 255), 3)
        # Show image
        color_filtering(img)
        cv2.imshow("Frame", img[...,::-1])
        # When you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()

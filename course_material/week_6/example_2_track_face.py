#!/usr/bin/env python
import cv2
import sys
from example_1_face_detector import FaceDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

#initalize camera
camera = Camera()
#initalize robot
robot = Robot()

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #start camera
    camera.start()
    #start robot
    robot.start()
    #initalize face detctor
    face_detector = FaceDetector()
    cnt = 0

    #loop
    while True:
        #gets image
        img = camera.getImage()
        #detects face and get image
        (img, centers) = face_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break
        # track ball every 50th frame
        cnt = cnt + 1
        if cnt % 50 == 0:
            if len(centers) > 0:
                #gets most recent center
                center = centers[0]
                #converts 2d coordinates to 3d coordinates on camera axis
                (x,y,z) = camera.convert2d_3d(center[0], center[1])
                print (x,y,z,'on camera axis')
                #converts 3d coordinates on camera axis to 3d coordinates on robot axis
                (x,y,z) = camera.convert3d_3d(x,y,z)
                print (x,y,z,'on robot axis')
                #move robot 
                robot.lookatpoint(x,y,z, 4, waitResult = False)

if __name__ == '__main__':
    main()

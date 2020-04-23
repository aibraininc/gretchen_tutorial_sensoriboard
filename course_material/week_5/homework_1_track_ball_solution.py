#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
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
    #initalize ball detector
    ball_detector = BallDetector()

    #count
    cnt = 0

    #loop
    while True:
        #TODO: get image from camera
        img = camera.getImage()
        #TODO: use ball_detector to detect ball
        (img, center) = ball_detector.detect(img, 640)
        #display
        cv2.imshow("Frame", img[...,::-1])

        key = cv2.waitKey(1)
        if key > 0:
            break

<<<<<<< HEAD:course_material/week_5/homework_1_track_ball_answer.py


=======
        #TODO: track ball with camera and robot lib
        cnt = cnt + 1
        if cnt % 50 == 0:
            print(center)
            if(center!= None):
                #converts 2d coordinates to 3d coordinates on camera axis
                (x,y,z) = camera.convert2d_3d(center[0], center[1])
                print (x,y,z,'on camera axis')
                #converts 3d coordinates on camera axis to 3d coordinates on robot axis
                (x,y,z) = camera.convert3d_3d(x,y,z)
                print (x,y,z,'on robot axis')
                #move robot to look at 3d point 
                robot.lookatpoint(x,y,z, 4, waitResult = False)
>>>>>>> be7a283c1d7a174d492b748b57d71f9593b9d9fa:course_material/week_5/homework_1_track_ball_solution.py

if __name__ == '__main__':
    main()
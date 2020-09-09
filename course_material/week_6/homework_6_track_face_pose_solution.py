#!/usr/bin/env python
import cv2
from example_2_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
import cv2
import numpy as np
import dlib
from imutils import face_utils
color_green = (0,255,0)
from lib.robot import Robot
import time

# global variable for frame_skip function
frame_skip_cnt = 0

# headInSquare function checks face is in sqaure or not
def headInSqaure(camera, face_x, face_y):
    isHeadInSquare = False
    if face_x >camera.width/2 - 60 and face_x <camera.width/2 + 60 and face_y >camera.height/2 - 60 and face_y <camera.height/2 + 60:
        isHeadInSquare = True
        return True
    return False

# frame_skip function skips the camera frames
def frame_skip(img):
    global frame_skip_cnt
    frame_skip_cnt = frame_skip_cnt +1
    if frame_skip_cnt %4 is not 0:
        return True
    return False


def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #start camera

    camera.start()

    robot = Robot()
    #start robot
    robot.start()
    #initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    dets = None
    Tracking = True
    #counter
    cnt = 0
    #loop
    while True:
        #get image
        img = camera.getImage()
        if frame_skip(img):
            continue

        #gets face detections
        dets = face_detector.detect(img)
        # when frame_skip_cnt is 4*n, it detects face 
        if len(dets)>0:

            face_tracking = None
            distanceFromCenter_min = 1000
            # find a face near image center
            for face in dets:
                face_x = (face.left()+face.right())/2
                face_y = (face.top()+face.bottom())/2

                #TODO: write a distance between face and center, center is 0.5*width of image.
                distanceFromCenter = abs(face_x - camera.width/2)

                if distanceFromCenter <distanceFromCenter_min:
                    distanceFromCenter_min = distanceFromCenter
                    face_tracking = face


            # Estimate pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, face_tracking)
            # Draw Rectangle
            cv2.rectangle(img,(face_tracking.left(), face_tracking.top()), (face_tracking.right(), face_tracking.bottom()), color_green, 3)
            # Draw pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)

            #TODO: When face is in square region, tracking is stop.
            if headInSqaure(camera,face_x,face_y):
                Tracking = False
                #TODO: remember current position
                print ("Pan angle is ",robot.getPosition()[0], "Tilt angle is", robot.getPosition()[1])
                current_pan = robot.getPosition()[0]
                current_tilt = robot.getPosition()[1]

            if Tracking:
                print("Keep tracking")
                #TODO: converts 2d coordinates to 3d coordinates on camera axis
                (x,y,z) = camera.convert2d_3d((face_tracking.left()+face_tracking.right())/2, (face_tracking.top()+face_tracking.bottom())/2)

                #TODO: converts 3d coordinates on camera axis to 3d coordinates on robot axis
                (x,y,z) = camera.convert3d_3d(x,y,z)

                #TODO: move robot to track your face
                robot.lookatpoint(x,y,z, 4)

            elif Tracking is False:
                yaw = rotation_vector[2]
                if yaw > 0.3:
                    print ('You are looking at right.')
                    #TODO: add motion for looking at right 
                    robot.move(0.8,0.5)
                    time.sleep(3)
                    robot.move(current_pan,current_tilt)
                #TODO: insert the condition for looking at left
                elif yaw < -0.3:
                    print ('You are looking at left.')
                    #TODO: add motion for looking at left 
                    robot.move(-0.8,0.5)
                    time.sleep(3)
                    robot.move(current_pan,current_tilt)

                print('Pause tracking until count is 50',cnt)
                cnt = cnt +1
                if cnt > 50:
                    Tracking = True
                    cnt = 0
        #show image
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()

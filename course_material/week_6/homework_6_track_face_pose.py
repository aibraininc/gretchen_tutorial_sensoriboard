#!/usr/bin/env python
import cv2
from example_2_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
import cv2
import numpy as np
from time import sleep
import dlib
from imutils import face_utils
color_green = (0,255,0)
from lib.robot import Robot
from time import time, sleep

# get current time (s)
def current_time():
    return time()

# global variable for frame_skip function
frame_skip_cnt = 0            #Get the x, y position


# headInSquare function checks face is in center of the image
def faceInCenter(camera, tracked_face_X, tracked_face_y, faceInCenter_count):
    # set boundaries
    left = 100
    right = 100
    up = 100
    bottom = 100

    if tracked_face_X >camera.width/2 - left and tracked_face_X <camera.width/2 + right and tracked_face_y >camera.height/2 - bottom and tracked_face_y <camera.height/2 + up:
        faceInCenter_count = faceInCenter_count + 1
        print "In Square"
    else:
        faceInCenter_count = 0
    return faceInCenter_count


# frame_skip function skips the camera frames
def frame_skip(img):
    global frame_skip_cnt
    frame_skip_cnt = frame_skip_cnt +1            
    if frame_skip_cnt %4 is not 0:
        return True
    return False

def main():
    faceInCenter_count = 0
    current_pan = 0
    current_tilt = 0
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #start camera
    camera.start()
    #Initalize robot
    robot = Robot()
    #start robot
    robot.start()
    #initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
    #face detection result
    dets = None
    # current tracking state
    Tracking = False
    # the time when motion for looking left/right runs
    motion_start_time = None
    cnt = 0
    
    #loop
    while True:
        #get image
        img = camera.getImage()
        if frame_skip(img):
            continue
        #gets detect face
        dets = face_detector.detect(img)

        #If the number ocurrent_panhe first face detected
        if(len(dets)>0):
            tracked_face  =  dets[0]
            #Get the x, y position
            tracked_face_x = (tracked_face.left()+tracked_face.right())/2
            tracked_face_y = (tracked_face.top()+tracked_face.bottom())/2

            # Estimate head pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, tracked_face)
            # Draw bounding box
            cv2.rectangle(img,(tracked_face.left(), tracked_face.top()), (tracked_face.right(), tracked_face.bottom()), color_green, 3)
            # Draw head pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)

            #Check if head is in the center, returns how many times the head was in the center
            faceInCenter_count =faceInCenter(camera, tracked_face_x, tracked_face_y, faceInCenter_count)
            print faceInCenter_count
            print ("{} in the center for {} times".format("Face as been", (faceInCenter_count))  )

            #We track whcurrent_panen the head is in the center for a certain period of time and there is not head motion activated
            if(faceInCenter_count<5 and motion_start_time == None):
                Tracking = True
            else:
                Tracking = False

            #Start tracking
            if Tracking:
                print("Tracking the Person")
                #TODO: converts the 2d point on the image  to a 3d point on camera coordinates system
                (x,y,z) = 
                #TODO: converts 3d point on camera coordinates system to 3d point on robot coordinates system
                (x,y,z) = 
                #TODO: move robot to track your face
                

            #When tracking is turned off, estimate the head pose and perform head motion if conditions meet
            elif Tracking is False:
                print "Stopped Tracking, Starting Head Pose Estimation"
                # yaw is angle of face on z-axis
                yaw = rotation_vector[2]

                #Condition for user looking towards the right
                if (yaw > 0.3 and motion_start_time == None):
                    print ('You are looking towards the right.')
                    #TODO: Remember the current position
                    current_position = 
                    current_pan = 
                    current_tilt = 
                    print "Starting head motion to look right"
                    #TODO: add motion for looking right
                    robot.move(,)
                    motion_start_time = current_time()

                #Condition for user looking towards the left
                elif (yaw < -0.3 and motion_start_time == None):
                    print ('You are looking towards the left.')
                    #TODO: Remember the current position
                    current_position =
                    current_pan = 
                    current_tilt = 
                    print "Starting head motion to look left"
                    #TODO: add motion for looking left
                    robot.move(,)
                    motion_start_time = current_time()

        #When head motion is activated we start the counter
        if(motion_start_time != None):
            print ("{} and its been {} seconds".format("Look motion activated ", (current_time()-motion_start_time))  )

        #After 3 seconds, we have to return to the current position
        if(motion_start_time != None and ((current_time()-motion_start_time) > 3) ):
            #Looking at the position that is stored.
            print "Robot is going back "
            #TODO: make the robot move to the stored current position
            robot.move(current_pan,current_tilt)
            motion_start_time = None
            #Tracking = True

        #Start tracking again
        if (cnt>10 and motion_start_time == None):
            Tracking = True
            cnt = cnt+1
        sleep(0.08)

        #show image
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break
if __name__ == '__main__':
    main()


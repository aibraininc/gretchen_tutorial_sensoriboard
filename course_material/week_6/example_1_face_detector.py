#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import imutils
from objects_msg.msg import Objects,Object
import dlib
from imutils import face_utils

class FaceDetector:
    def __init__(self):
        #initalize detector
        self.detector = dlib.get_frontal_face_detector()
        #Initalize predictor for pose estimation(landmarks)

    #detect face
    def detect(self, frame):
        # 1. resize the frame, and convert it to the HSV
        rects = self.detector(frame, 1)
        return rects


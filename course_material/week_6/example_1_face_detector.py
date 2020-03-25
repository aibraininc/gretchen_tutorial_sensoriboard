#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import imutils
from objects_msg.msg import Objects,Object

class FaceDetector:
    def __init__(self):
        rospy.Subscriber("/gazr/face", Objects, self.objectCallback, queue_size = 1000)
        self.faces = []

    def objectCallback(self, data):
        self.faces= data.objects

    def detect(self, frame, _width):
        # 1. resize the frame, and convert it to the HSV
        frame = imutils.resize(frame, width= _width)
        faces = self.faces
        centors = []
        for face in faces:
            centor = (int(face.u),int(face.v))
            centors.append(centor)
            cv2.circle(frame, centor, 100, (0, 0, 255),5)
        return [frame,centors]
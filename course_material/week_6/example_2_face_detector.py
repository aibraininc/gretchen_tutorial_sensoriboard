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
        # Initalize detector
        self.detector = dlib.get_frontal_face_detector()
        # Initalize predictor for pose estimation(landmarks)
        self.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
        # Create camera matrix
        focal_length = 640
        center = (640/2, 480/2)
        self.camera_matrix = np.array(
                                     [[focal_length, 0, center[0]],
                                     [0, focal_length, center[1]],
                                     [0, 0, 1]], dtype = "double"
                                     )
        self.dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
        print ("Camera Matrix :\n {0}".format(self.camera_matrix))

    # Detect face
    def detect(self, frame):
        # 1. resize the frame, and convert it to the HSV
        rects = self.detector(frame, 1)
        return rects
    def estimate_pose(self,frame, rect):
        # Use shape predictor to predict the location of the landmark
        shape0 = self.predictor(frame, rect)
        # Convert to numpy
        shape0 = np.array(face_utils.shape_to_np(shape0))
        # 2D image points of detected face
        image_points = np.array([
                                        (shape0[33, :]),     # Nose tip
                                        (shape0[8,  :]),     # Chin
                                        (shape0[36, :]),     # Left eye left corner
                                        (shape0[45, :]),     # Right eye right corne
                                        (shape0[48, :]),     # Left Mouth corner
                                        (shape0[54, :])      # Right mouth corner
                                    ], dtype="double")

        # 3D model points of the face model.
        model_points = np.array([
                                        (0.0, 0.0, 0.0),             # Nose tip
                                        (0.0, -330.0, -65.0),        # Chin
                                        (-225.0, 170.0, -135.0),     # Left eye left corner
                                        (225.0, 170.0, -135.0),      # Right eye right corne
                                        (-150.0, -150.0, -125.0),    # Left Mouth corner
                                        (150.0, -150.0, -125.0)      # Right mouth corner
                                    ])
        # Solve for pnp
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        print ("Rotation Vector:\n {0}".format(rotation_vector))
        print ("Translation Vector:\n {0}".format(translation_vector))
        return (success, rotation_vector, translation_vector, image_points)
    # Draw pose
    def draw_pose(self,frame, rotation_vector, translation_vector, image_points):
        # 3D point (0, 0, 1000.0) is projected on to the image plane
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, self.camera_matrix, self.dist_coeffs)
        for p in image_points:
            cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0,0,255), -1)
        p1 = ( int(image_points[0][0]), int(image_points[0][1]))
        p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        cv2.line(frame, p1, p2, (255,0,0), 2)
        return frame

#!/usr/bin/env python
import cv2
import sys
from example_1_face_detector import FaceDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
camera = Camera()
robot = Robot()


def main():
    ROSEnvironment()
    camera.start()
    robot.start()
    face_detector = FaceDetector()
    cnt = 0

    while True:
        img = camera.getImage()
        (img, centors) = face_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break
        # track ball
        cnt = cnt + 1
        if cnt % 50 == 0:
            if len(centors) > 0:
                centor = centors[0]
                (x,y,z) = camera.convert2d_3d(centor[0], centor[1])
                print (x,y,z,'on camera axis')
                (x,y,z) = camera.convert3d_3d(x,y,z)
                print (x,y,z,'on robot axis')
                robot.lookatpoint(x,y,z, 4, waitResult = False)

if __name__ == '__main__':
    main()





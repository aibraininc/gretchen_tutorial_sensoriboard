#!/usr/bin/env python


import rospy
import roslib
from lib.robot import Robot
from lib.camera import Camera
from lib.ball_detector import BallDetector

class BallTrackingSystem:

    def __init__(self):
        self.initParam()
        self.pan_speed = 0
        self.tilt_speed = 0

        # init 
        self.robot = Robot()
        self.ball_detector = BallDetector()
        self.camera = Camera(self.imageCallback)

        # move robot head to center
        self.robot.center()

        # load timer
        rospy.Timer(rospy.Duration(1.0/self.rate), self.robotUpdate)

    def robotUpdate(self, event):
        # self.robot.test()
        self.robot.move(self.pan_speed, self.tilt_speed)

    def imageCallback(self, frame):
        results = self.ball_detector.detect(frame, 640)
        frame = results[0]
        if results[1] != None:
            self.set_joint_cmd(results)
        return frame


    def set_joint_cmd(self, msg):

        ball = msg[1]
        frame = msg[0]
        (image_height, image_width) = frame.shape[:2]

        target_offset_x = ball[0] - image_width / 2
        target_offset_y = ball[1] - image_height / 2
    
        try:
            percent_offset_x = float(target_offset_x) / (float(image_width) / 2.0)
            percent_offset_y = float(target_offset_y) / (float(image_height) / 2.0)
        except:
            percent_offset_x = 0
            percent_offset_y = 0

        if abs(percent_offset_x) > self.pan_threshold:
            if target_offset_x > 0:
                self.pan_speed = min(self.max_joint_speed, max(0, self.gain_pan * abs(percent_offset_x)))
            else:            
                self.pan_speed = -1 *min(self.max_joint_speed, max(0, self.gain_pan * abs(percent_offset_x)))
        else:
            self.pan_speed = 0

        if abs(percent_offset_y) > self.tilt_threshold:
            if target_offset_y > 0:
                self.tilt_speed = min(self.max_joint_speed, max(0, self.gain_tilt * abs(percent_offset_y)))
            else:            
                self.tilt_speed = -1 *min(self.max_joint_speed, max(0, self.gain_tilt * abs(percent_offset_y)))
        else:
            self.tilt_speed = 0



    def initParam(self):
        self.rate = rospy.get_param("~rate", 20)

        # Joint speeds are given in radians per second
        self.max_joint_speed = rospy.get_param('~max_joint_speed', 0.1)

        # The pan/tilt thresholds indicate what percentage of the image window
        # the ROI needs to be off-center before we make a movement
        self.pan_threshold = rospy.get_param("~pan_threshold", 0.05)
        self.tilt_threshold = rospy.get_param("~tilt_threshold", 0.05)
        
        # The gain_pan and gain_tilt parameter determine how responsive the
        # servo movements are. If these are set too high, oscillation can result.
        self.gain_pan = rospy.get_param("~gain_pan", 1.0)
        self.gain_tilt = rospy.get_param("~gain_tilt", 1.0)

        self.max_pan_angle_radian = rospy.get_param("~max_pan_angle_radian", 1.0)
        self.max_tilt_angle_radian = rospy.get_param("~max_tilt_angle_radian", 1.0)



def main():
    rospy.init_node('ball_tracking', anonymous=True)
    system = BallTrackingSystem()
    while not rospy.is_shutdown():
        rospy.spin()
if __name__ == '__main__':
    main()

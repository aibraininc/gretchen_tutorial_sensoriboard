#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import String

class AICoRE:

    def __init__(self):
        print('AICore Client')
        self.inputTextPub = rospy.Publisher("/aicore/input", String, queue_size = 10)
        self.namePub = rospy.Publisher("/aicore/username", String, queue_size = 10)
        rospy.Subscriber("/aicore/output", String, self.outputCallback, queue_size = 1000)
        rospy.sleep(3)

    def setUserName(self, name):
        d = String()
        d.data = name
        self.namePub.publish(d)
        print('You set the username as '+name)
        rospy.sleep(1)

    def send(self, text):
        d = String()
        d.data = text
        self.inputTextPub.publish(d)
        print(text)
    
    def answer(self):
        msg=rospy.wait_for_message('/aicore/output', String)
        self.result = str(msg.data)
        print(self.result)
        return self.result

    def outputCallback(self, msg):
        pass
        
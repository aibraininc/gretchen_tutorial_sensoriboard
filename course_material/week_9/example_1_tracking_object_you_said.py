#!/usr/bin/env python

# once you say a object, robot looks at the object.

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import speech_recognition as sr
import cv2
import argparse
import numpy as np
print(cv2.__version__)
sys.path.append('..')

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import rospy
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
from lib.robot import Robot


#Path to files needed
cfg_path = "./yolov3-tiny.cfg"
weight_path= "./yolov3-tiny.weights"
class_name_path = "./yolov3.txt"


#Loads class names into an array
classes = None
with open(class_name_path, 'r') as file:
    classes = [line.strip() for line in file.readlines()]
print classes

#Creates different color for different colors
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


#draws bounding box on the image
def draw_boundingbox(img, class_id, confidence, x, y, x_end, y_end):
    class_name = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (int(x), int(y)), (int(x_end) ,int(y_end)), color, 2)
    cv2.putText(img, class_name, (int(x-10),int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# find a class in sentence
# classes is yolo-classes
def senetenceParsing(sentence = 'look at a bottle'):
    sentence = sentence.lower()
    for word in classes:
        if word in sentence:
            return word

def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    robot = Robot()
    robot.start()

    r = sr.Recognizer()
    mic = sr.Microphone(device_index=11)
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    text = r.recognize_google(audio)
    print(text)
    object_to_track = senetenceParsing(text)
    print(object_to_track)
    if object_to_track == None:
        object_to_track = 'bottle'

    #loops
    while(True):
        #gets image from camera
        cam_image = camera.getImage()

        #Gets width and height of image
        input_image = cam_image
        width = input_image.shape[1]
        height = input_image.shape[0]

        #Loads deep neural network with weight and configure file
        net = cv2.dnn.readNet(weight_path, cfg_path)

        #creates a "bob" that is the input image after mean subtraction, normalizing, channel swapping
        #0.00392 is the scale factor
        #(416,416) is the size of the output image
        #(0,0,0) are the mean values that will be subtracted for each channel RGB
        blob = cv2.dnn.blobFromImage(input_image, 0.00392, (416,416), (0,0,0), True, crop=False)

        #Inputs blob into the neural network
        net.setInput(blob)

        #gets the output layers "yolo_82', 'yolo_94', 'yolo_106"
        #output layer contains the detection/prediction information
        layer_names = net.getLayerNames()
        #getUnconnectedOutLayers() returns indices of unconnected layers
        #layer_names[i[0] - 1] gets the name of the layers of the indices
        #net.getUnconnectedOutLayers() returns [[200], [227], [254]]
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        #Runs forward pass to compute output of layer
        #returns predictions/detections at 32, 16 and 8 scale
        preds = net.forward(output_layers)

        #Initialize list that contains class id, confidence values, bounding boxes
        class_ids = []
        confidence_values = []
        bounding_boxes = []

        #Initialize confidence threshold and threshold for non maximal suppresion
        conf_threshold = 0.5
        nms_threshold = 0.4

        #for each scale, we go through the detections
        for pred in preds:
            for detection in pred:
                #Use the max score as confidence
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                #Check if confidence is greather than threshold
                if confidence > conf_threshold:
                    #Compute x,y, widht, height, class id, confidence value
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidence_values.append(float(confidence))
                    bounding_boxes.append([x, y, w, h])

        #perform non maximal suppression
        indices = cv2.dnn.NMSBoxes(bounding_boxes, confidence_values, conf_threshold, nms_threshold)

        #draw results
        #tracked_object flag for if object is already tracked
        tracked_object = 0
        for i in indices:
            i = i[0]
            box = bounding_boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            center_x = x+w/2.0
            center_y = y+h/2.0
            classid = class_ids[i]
            class_name = str(classes[classid])
            #If detected object equals to the object tracked
            if(class_name ==  object_to_track and tracked_object == 0):
                #Converts the 3d camera coordinates into 3d world coordinates
                (x_3d,y_3d,z_3d) = camera.convert2d_3d(center_x, center_y)
                (x_3d,y_3d,z_3d) = camera.convert3d_3d(x_3d,y_3d,z_3d)
                #commands the robot to look
                robot.lookatpoint(x_3d,y_3d,z_3d, 4, waitResult = False)
                tracked_object = 1
                print("Traking"+class_name)
            print(class_name)
            conf_value = confidence_values[i]
            draw_boundingbox(input_image, classid, conf_value, round(x), round(y), round(x+w), round(y+h))

        cv2.imshow("Object Detection Window", input_image[...,::-1])
        key = cv2.waitKey(1)
        cv2.imwrite("detected_object.jpg", input_image)
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()

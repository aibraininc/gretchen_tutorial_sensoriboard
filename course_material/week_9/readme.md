## install

* roscd course_material/week_9
* virtualenv -p python myenv
* source myenv/bin/activate
* pip install SpeechRecognition
* pip install pyYAML
* pip install opencv-python
* pip install opencv-contrib-python
* pip install netifaces
* pip install rospkg
* pip install pyaudio


## example
* roslaunch course_material init_device.launch
* rosrun aibrain_ros_java aicore_client com.github.rosjava.aibrain_ros_java.aicore_client.AICoreClient
(select option 2)
* source myenv/bin/activate
* python example_2_tracking_object_you_said_v2.py 
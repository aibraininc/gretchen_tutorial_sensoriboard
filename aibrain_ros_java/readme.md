
## speech recognizer and tts
cd
source env/bin/activate
python Desktop/fiona_speech_recognition/assistant.py

## aicore server
cd /home/aibrain/AICoRe/AICoRe/AICoReServer/AICoREServer
sh runAICoREjar.sh stop
sh runAICoREjar.sh start


## aicore client
/home/aibrain/myjava/src/aibrain_ros_java/aicore_client/build/install/aicore_client/bin/aicore_client com.github.rosjava.aibrain_ros_java.aicore_client.AICoreClient


## ask detect speech
rostopic pub /keyboard_input std_msgs/String "data: ''"
## send recognized speech
rostopic pub /recognized_speech std_msgs/String "data: 'Text'"


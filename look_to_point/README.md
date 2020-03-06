# [tutorial] 1. look to point 

## example
- roslaunch look_to_point start_look_to_point.launch 
- rostopic pub /look_point std_msgs/String "data: 'B'" 

# [tutorial] 2. detect objects and save the objects on the map (yolo)

## installation

- cd catkin_workspace/src
- catkin_make -DCMAKE_BUILD_TYPE=Release

## example

- roslaunch look_to_point detect_object_and_save.launch 
- rosrun look_to_point save_objects_to_map_with_yolo 
- roslaunch look_to_point start_look_to_point.1.launch
- roslaunch darknet_ros yolo_v3.launch 
- rosrun map_manager map_manager_without_db.py
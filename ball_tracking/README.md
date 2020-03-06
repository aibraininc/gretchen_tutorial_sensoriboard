# ball-tracking

## [tutorial] 1. test control by key_teleop

- roslaunch ball_tracking start_init.launch
- rosrun key_teleop key_teleop.py
- rosrun ball_tracking key_op.py

## [tutorial] 2. track green object (simple)

- roslaunch ball_tracking start_init.launch
- roslaunch ball_tracking ball_tracker_simple.launch

## [tutorial] 3. track green object (callback)

- roslaunch ball_tracking start_init.launch
- roslaunch ball_tracking ball_tracker_callback.launch

# ball tracking parameters

in launch file, there is a param setting.

rate is the frequency of motor control update calls. The higher the rate, the more updates are called.

- rate: 20 

The position of the object is represented by a value between -1 and 1. The threshold checks how far from the center it is.

- pan_threshold: 0.05
- tilt_threshold: 0.05


gain is a parameter used to adjust the speed of the motor. The speed of the motor is offset * gain. offset is the position of obstacle.

- gain_pan: 0.05
- gain_tilt: 0.05

The speed of the motor does not exceed max_joint_speed.

- max_joint_speed: 0.1

limit is the maximum angle of the motor.

- max_pan_angle_radian: 1.0
- max_tilt_angle_radian: 1.0

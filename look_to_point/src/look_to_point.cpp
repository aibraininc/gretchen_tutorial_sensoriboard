
// C++ standard headers
#include <exception>
#include <string>

// Boost headers
#include <boost/shared_ptr.hpp>

// ROS headers
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <actionlib/client/simple_action_client.h>
#include <sensor_msgs/CameraInfo.h>
#include <geometry_msgs/PointStamped.h>
#include <control_msgs/PointHeadAction.h>
#include <sensor_msgs/image_encodings.h>
#include <ros/topic.h>

#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h>


// OpenCV headers
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>

#include <tf_conversions/tf_kdl.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>

static std::string windowName      = "image";
static std::string cameraFrame     = "/camera_color_optical_frame";
static std::string imageTopic      = "/camera/color/image_raw";
static std::string cameraInfoTopic = "/camera/color/camera_info";

// Intrinsic parameters of the camera
cv::Mat cameraIntrinsics;

typedef actionlib::SimpleActionClient<control_msgs::PointHeadAction> PointHeadClient;
typedef boost::shared_ptr<PointHeadClient> PointHeadClientPtr;

PointHeadClientPtr pointHeadClient;
tf::TransformListener * tfl_;
ros::Time latestImageStamp;

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void looktopoint(float x, float y, float z, float velocity, bool wait)
{
  geometry_msgs::PointStamped pointStamped;
  pointStamped.header.frame_id = cameraFrame;
  pointStamped.header.stamp    = latestImageStamp;
  control_msgs::PointHeadGoal goal;
  goal.pointing_frame = cameraFrame;
  goal.pointing_axis.x = 0.0;
  goal.pointing_axis.y = 0.0;
  goal.pointing_axis.z = 1.0;
  goal.min_duration = ros::Duration(0.2);
  goal.max_velocity = velocity;
  goal.target = pointStamped;
  goal.target.point.x = x;
  goal.target.point.y = y;
  goal.target.point.z = z;

  pointHeadClient->sendGoal(goal);
  if(wait)
    bool actionOk = pointHeadClient->waitForResult(ros::Duration(10));
}

void testCallback2(const std_msgs::Float32MultiArray& test) {

  ROS_INFO_STREAM(test.data[0]);
  ROS_INFO_STREAM(test.data[1]);
  ROS_INFO_STREAM(test.data[2]);
  looktopoint(test.data[0], test.data[1], test.data[2], 0.3, false);
}

void testCallback(const std_msgs::String& test)
{
  ROS_INFO_STREAM(test.data);
  geometry_msgs::PointStamped pointStamped;
  pointStamped.header.frame_id = cameraFrame;
  pointStamped.header.stamp    = latestImageStamp;
  control_msgs::PointHeadGoal goal;
  goal.pointing_frame = cameraFrame;
  goal.pointing_axis.x = 0.0;
  goal.pointing_axis.y = 0.0;
  goal.pointing_axis.z = 1.0;
  goal.min_duration = ros::Duration(0.2);
  goal.max_velocity = 1.0;
  goal.target = pointStamped;

  if(test.data == "A") {
    goal.target.point.x = 0.810009;
    goal.target.point.y = 0.544378;
    goal.target.point.z = 0.336105;
    pointHeadClient->sendGoal(goal);
    ros::Duration(0.5).sleep();
  }
  else if(test.data == "B") {
    goal.target.point.x = 0.986182;
    goal.target.point.y = -0.171377;
    goal.target.point.z = 0.166996;
    pointHeadClient->sendGoal(goal);
    ros::Duration(0.5).sleep();
  }
  else if(test.data == "C") {
    looktopoint(0.387198, 0.981229, 0.040284, 0.35, true);
    ros::Duration(0.1).sleep();
    looktopoint(0.746435, -0.731782, -0.095392, 0.35, true);
    ros::Duration(0.1).sleep();
    looktopoint(0.999216, -0.0368807, 0.346798, 0.4, true);
  }
}




control_msgs::PointHeadGoal convertGoaltoGoalFromBase(control_msgs::PointHeadGoal goal){
		// get root_, pan_link_, pointing_frame_
		ros::Time now = ros::Time::now();
		std::string root_ = "base_link";
		std::string pan_link_ = "pan_link";

		tfl_->getParent(pan_link_, ros::Time(), root_);
		if (root_[0] == '/') root_.erase(0, 1);
		std::string pointing_frame_ = goal.pointing_frame;
		if (pointing_frame_[0] == '/') pointing_frame_.erase(0, 1);

		//--------------------------------------------------------------
		bool ret1 = tfl_->waitForTransform(pan_link_, pointing_frame_, goal.target.header.stamp,
                                     ros::Duration(5.0), ros::Duration(0.01));
		tf::Vector3 pointing_axis_;
		tf::vector3MsgToTF(goal.pointing_axis, pointing_axis_);
		pointing_axis_.normalize(); // 0,0,1 z-axis

		// get target_in_root, from base to xtion
		tf::Point target_in_root_;
		ret1 = tfl_->waitForTransform(root_.c_str(), goal.target.header.frame_id, goal.target.header.stamp,
		                                       ros::Duration(5.0), ros::Duration(0.01));
		geometry_msgs::PointStamped target_in_root_msg;

    ROS_INFO_STREAM("Frame : " << root_.c_str()); // base_link
    ROS_INFO_STREAM("Goal from camera: " << goal.target); // frame_id is /camera_color_optical_frame, point

		tfl_->transformPoint(root_.c_str(), goal.target, target_in_root_msg );

    ROS_INFO_STREAM("Goal from base : " << target_in_root_msg);


		tf::pointMsgToTF(target_in_root_msg.point, target_in_root_);
		ROS_INFO_STREAM("Target point in base frame: (" << target_in_root_[0] << ", " << target_in_root_[1] << ", " << target_in_root_[2] << ")");
		ROS_INFO_STREAM("[" << target_in_root_[0] << ", " << target_in_root_[1] << ", " << target_in_root_[2] << "]");
		goal.target.point.x = target_in_root_[0];
		goal.target.point.y = target_in_root_[1];
		goal.target.point.z = target_in_root_[2];


		return goal;
}


// ROS call back for every new image received
void imageCallback(const sensor_msgs::ImageConstPtr& imgMsg)
{
  latestImageStamp = imgMsg->header.stamp;

  cv_bridge::CvImagePtr cvImgPtr;

  cvImgPtr = cv_bridge::toCvCopy(imgMsg, sensor_msgs::image_encodings::BGR8);
  cv::imshow(windowName, cvImgPtr->image);
  cv::waitKey(15);
}

// OpenCV callback function for mouse events on a window
void onMouse( int event, int u, int v, int, void* )
{
  if ( event != cv::EVENT_LBUTTONDOWN )
      return;

  ROS_INFO_STREAM("Pixel selected (" << u << ", " << v << ")");

  geometry_msgs::PointStamped pointStamped;

  pointStamped.header.frame_id = cameraFrame;
  pointStamped.header.stamp    = latestImageStamp;

  //compute normalized coordinates of the selected pixel
  double x = ( u  - cameraIntrinsics.at<double>(0,2) )/ cameraIntrinsics.at<double>(0,0);
  double y = ( v  - cameraIntrinsics.at<double>(1,2) )/ cameraIntrinsics.at<double>(1,1);
  double Z = 1.0; //define an arbitrary distance
  pointStamped.point.x = x * Z;
  pointStamped.point.y = y * Z;
  pointStamped.point.z = Z;

  ROS_INFO_STREAM("Target point in camera frame: (" << x * Z << ", " << y * Z << ", " << Z << ")");

  //build the action goal
  control_msgs::PointHeadGoal goal;
  //the goal consists in making the Z axis of the cameraFrame to point towards the pointStamped
  goal.pointing_frame = cameraFrame;
  goal.pointing_axis.x = 0.0;
  goal.pointing_axis.y = 0.0;
  goal.pointing_axis.z = 1.0;
  goal.min_duration = ros::Duration(0.2);
  goal.max_velocity = 0.6;
  goal.target = pointStamped;

  pointHeadClient->sendGoal(convertGoaltoGoalFromBase(goal));
  ros::Duration(0.5).sleep();
}

void createPointHeadClient(PointHeadClientPtr& actionClient)
{
  ROS_INFO("Creating action client to head controller ...");

  actionClient.reset( new PointHeadClient("/head_controller/absolute_point_head_action") );

  int iterations = 0, max_iterations = 3;
  // Wait for head controller action server to come up
  while( !actionClient->waitForServer(ros::Duration(2.0)) && ros::ok() && iterations < max_iterations )
  {
    ROS_DEBUG("Waiting for the point_head_action server to come up");
    ++iterations;
  }

  if ( iterations == max_iterations )
    throw std::runtime_error("Error in createPointHeadClient: head controller action server not available");
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Entry point
int main(int argc, char** argv)
{
  // Init the ROS node
  ros::init(argc, argv, "look_to_point");
  tfl_ = new tf::TransformListener();

  ROS_INFO("Starting look_to_point application ...");

  // Precondition: Valid clock
  ros::NodeHandle nh;
  if (!ros::Time::waitForValid(ros::WallDuration(10.0))) // NOTE: Important when using simulated clock
  {
    ROS_FATAL("Timed-out waiting for valid time.");
    return EXIT_FAILURE;
  }

  // Get the camera intrinsic parameters from the appropriate ROS topic
  ROS_INFO("Waiting for camera intrinsics ... ");
  sensor_msgs::CameraInfoConstPtr msg = ros::topic::waitForMessage
      <sensor_msgs::CameraInfo>(cameraInfoTopic, ros::Duration(10.0));
  if(msg.use_count() > 0)
  {
    cameraIntrinsics = cv::Mat::zeros(3,3,CV_64F);
    cameraIntrinsics.at<double>(0, 0) = msg->K[0]; //fx
    cameraIntrinsics.at<double>(1, 1) = msg->K[4]; //fy
    cameraIntrinsics.at<double>(0, 2) = msg->K[2]; //cx
    cameraIntrinsics.at<double>(1, 2) = msg->K[5]; //cy
    cameraIntrinsics.at<double>(2, 2) = 1;
  }

  // load yaml
  nh.param("cameraFrame", cameraFrame, std::string("/camera_color_optical_frame"));
  nh.param("imageTopic", imageTopic, std::string("/camera/color/image_raw"));
  nh.param("cameraInfoTopic", cameraInfoTopic, std::string("/camera/color/camera_info"));

  createPointHeadClient( pointHeadClient );

  cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);

  // Set mouse handler for the window
  cv::setMouseCallback(windowName, onMouse);

  image_transport::ImageTransport it(nh);
  // use compressed image transport to use less network bandwidth
  image_transport::TransportHints transportHint("compressed");

  ROS_INFO_STREAM("Subscribing to " << imageTopic << " ...");
  image_transport::Subscriber sub = it.subscribe(imageTopic, 1,
                                                 imageCallback, transportHint);

	ros::Subscriber testSub = nh.subscribe("/look_point", 1, testCallback);
	ros::Subscriber testSub2 = nh.subscribe("/look_at_point", 10, testCallback2);


  //enter a loop that processes ROS callbacks. Press CTRL+C to exit the loop
  ros::spin();

  cv::destroyWindow(windowName);

  return EXIT_SUCCESS;
}

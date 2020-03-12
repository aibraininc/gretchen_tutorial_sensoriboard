
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
#include <visualization_msgs/Marker.h>

// OpenCV headers
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>

#include <tf_conversions/tf_kdl.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>


// custom message
#include "objects_msg/Object.h"
#include "objects_msg/Objects.h"
#include <darknet_ros_msgs/BoundingBoxes.h>
#include <darknet_ros_msgs/BoundingBox.h>

static const std::string windowName      = "image";
static const std::string cameraFrame     = "/camera_color_optical_frame";
static const std::string imageTopic      = "/camera/color/image_raw";
static const std::string cameraInfoTopic = "/camera/color/camera_info";

// Intrinsic parameters of the camera
cv::Mat cameraIntrinsics;

typedef actionlib::SimpleActionClient<control_msgs::PointHeadAction> PointHeadClient;
typedef boost::shared_ptr<PointHeadClient> PointHeadClientPtr;

tf::TransformListener * tfl_;
ros::Time latestImageStamp;

ros::Publisher vis_pub;
ros::Publisher look_at_point_pub;
int vis_id =0;
int bounding_box_cnt = 0;

objects_msg::Object constructObjectWithYolo(darknet_ros_msgs::BoundingBox& box, visualization_msgs::Marker& marker) {
  objects_msg::Object obj;
  obj.id = 0;
  obj.tag = boost::to_string(box.id);
  obj.tagName = box.Class;
  obj.x = marker.pose.position.x;
  obj.y = marker.pose.position.y;
  obj.z = marker.pose.position.z;
  obj.xmin = box.xmin;
  obj.xmax = box.xmax;
  obj.ymin = box.ymin;
  obj.ymax = box.ymax;
  obj.side = 0;

  return obj;
}


objects_msg::Object constructObject(visualization_msgs::Marker& marker) {
  objects_msg::Object obj;
  std::cout<<"vis_id"<<vis_id<<std::endl;
  obj.id = 0;
  obj.tag = "0";
  obj.tagName = "Hello";
  obj.x = marker.pose.position.x;
  obj.y = marker.pose.position.y;
  obj.z = marker.pose.position.z;
  return obj;
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

    // ROS_INFO_STREAM("Frame : " << root_.c_str()); // base_link
    // ROS_INFO_STREAM("Goal from camera: " << goal.target); // frame_id is /camera_color_optical_frame, point

		tfl_->transformPoint(root_.c_str(), goal.target, target_in_root_msg );

    // ROS_INFO_STREAM("Goal from base : " << target_in_root_msg);


		tf::pointMsgToTF(target_in_root_msg.point, target_in_root_);
		goal.target.point.x = target_in_root_[0];
		goal.target.point.y = target_in_root_[1];
		goal.target.point.z = target_in_root_[2];
		return goal;
}


void boundingBoxCallback(const darknet_ros_msgs::BoundingBoxes msg) {
  bounding_box_cnt++;
  // if(bounding_box_cnt %5 == 0) {
    int cnt = msg.bounding_boxes.size();
    int cntObjectWithDepth = 0;
    objects_msg::Objects new_obj_list;
    new_obj_list.image_header = msg.image_header;

    for(size_t i = 0; i < cnt; i++)
    {
      darknet_ros_msgs::BoundingBox box = msg.bounding_boxes[i];
      int u = (box.xmin + box.xmax) / 2;
      int v = (box.ymin + box.ymax) / 2;
      float z = box.depth; // should get depth

      geometry_msgs::PointStamped pointStamped;
      pointStamped.header.frame_id = cameraFrame;
      pointStamped.header.stamp    = msg.image_header.stamp;

      double x = ( u  - cameraIntrinsics.at<double>(0,2) )/ cameraIntrinsics.at<double>(0,0);
      double y = ( v  - cameraIntrinsics.at<double>(1,2) )/ cameraIntrinsics.at<double>(1,1);
      double Z = z; //define an arbitrary distance
      if(Z == 0)
      {
        continue;
      }
      pointStamped.point.x = x * Z;
      pointStamped.point.y = y * Z;
      pointStamped.point.z = Z;   

      //build the action goal
      control_msgs::PointHeadGoal goal;
      //the goal consists in making the Z axis of the cameraFrame to point towards the pointStamped
      goal.pointing_frame = cameraFrame;
      goal.pointing_axis.x = 0.0;
      goal.pointing_axis.y = 0.0;
      goal.pointing_axis.z = 1.0;
      goal.min_duration = ros::Duration(1.0);
      goal.max_velocity = 0.25;
      goal.target = pointStamped;

      control_msgs::PointHeadGoal goal_from_base = convertGoaltoGoalFromBase(goal);

      visualization_msgs::Marker marker;
      marker.header.frame_id = "/base_link";
      marker.header.stamp = ros::Time();
      marker.ns = "hi_hello";
      marker.id = bounding_box_cnt;
      marker.lifetime = ros::Duration(2.0);
      marker.type = visualization_msgs::Marker::SPHERE;
      marker.action = visualization_msgs::Marker::ADD;
      marker.pose.position.x = goal_from_base.target.point.x;
      marker.pose.position.y = goal_from_base.target.point.y;
      marker.pose.position.z = goal_from_base.target.point.z;
      marker.pose.orientation.x = 0.0;
      marker.pose.orientation.y = 0.0;
      marker.pose.orientation.z = 0.0;
      marker.pose.orientation.w = 1.0;
      marker.scale.x = 0.1;
      marker.scale.y = 0.1;
      marker.scale.z = 0.1;
      marker.color.a = 1.0; // Don't forget to set the alpha!
      marker.color.r = 1.0;
      marker.color.g = 0.0;
      marker.color.b = 1.0;
      //only if using a MESH_RESOURCE marker type:
      vis_pub.publish( marker );
      new_obj_list.objects.push_back(constructObjectWithYolo(box, marker));
      cntObjectWithDepth++;
    }
    new_obj_list.cnt = cntObjectWithDepth;
    look_at_point_pub.publish(new_obj_list);
  // }

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

  ROS_INFO_STREAM("Pixel selected (" << u << ", " << v << ")");\

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
  goal.min_duration = ros::Duration(1.0);
  goal.max_velocity = 0.25;
  goal.target = pointStamped;

  control_msgs::PointHeadGoal goal_from_base = convertGoaltoGoalFromBase(goal);

  visualization_msgs::Marker marker;
  marker.header.frame_id = "/base_link";
  marker.header.stamp = ros::Time();
  marker.ns = "hello";
  marker.id = vis_id++;
  marker.type = visualization_msgs::Marker::SPHERE;
  marker.action = visualization_msgs::Marker::ADD;
  marker.pose.position.x = goal_from_base.target.point.x;
  marker.pose.position.y = goal_from_base.target.point.y;
  marker.pose.position.z = goal_from_base.target.point.z;
  marker.pose.orientation.x = 0.0;
  marker.pose.orientation.y = 0.0;
  marker.pose.orientation.z = 0.0;
  marker.pose.orientation.w = 1.0;
  marker.scale.x = .1;
  marker.scale.y = 0.1;
  marker.scale.z = 0.1;
  marker.color.a = 1.0;
  marker.color.r = 1.0;
  marker.color.g = 0.0;
  marker.color.b = 0.0;
  vis_pub.publish( marker );

  objects_msg::Objects lookat;
  lookat.cnt = 1;
  lookat.objects.push_back(constructObject(marker));
  look_at_point_pub.publish(lookat);

  std_msgs::String a;
  a.data = "";
  ros::Duration(0.5).sleep();
}

// Entry point
int main(int argc, char** argv)
{
  // Init the ROS node
  ros::init(argc, argv, "look_to_point2");
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

  // cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);

  // // Set mouse handler for the window
  // cv::setMouseCallback(windowName, onMouse);

  // image_transport::ImageTransport it(nh);
  // // use compressed image transport to use less network bandwidth
  // image_transport::TransportHints transportHint("compressed");

  // ROS_INFO_STREAM("Subscribing to " << imageTopic << " ...");
  // image_transport::Subscriber sub = it.subscribe(imageTopic, 1,
  //                                                imageCallback, transportHint);

	ros::Subscriber darknetObjectSub = nh.subscribe("/darknet_ros/bounding_boxes", 10, boundingBoxCallback);

  vis_pub = nh.advertise<visualization_msgs::Marker>( "visualization_marker", 0 );
  look_at_point_pub = nh.advertise<objects_msg::Objects>("/athena/objects", 1);

  ros::spin();

  cv::destroyWindow(windowName);

  return EXIT_SUCCESS;
}

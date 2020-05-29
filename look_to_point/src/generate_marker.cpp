// ROS headers
#include <ros/ros.h>
#include <ros/topic.h>
#include <visualization_msgs/Marker.h>


ros::Publisher vis_pub;
int vis_id =0;

// OpenCV callback function for mouse events on a window
void makeMakrer(float x, float y, float z, int id)
{
  visualization_msgs::Marker marker;
  marker.header.frame_id = "/base_link";
  marker.header.stamp = ros::Time();
  marker.ns = "hello";
  marker.id = id;
  marker.type = visualization_msgs::Marker::CUBE;
  marker.action = visualization_msgs::Marker::ADD;
  marker.pose.position.x = x;
  marker.pose.position.y = y;
  marker.pose.position.z = z;
  marker.pose.orientation.x = 0.0;
  marker.pose.orientation.y = 0.0;
  marker.pose.orientation.z = 0.0;
  marker.pose.orientation.w = 1.0;
  marker.scale.x = .1;
  marker.scale.y = 0.1;
  marker.scale.z = 0.1;
  marker.color.a = 1.0;

  if(id ==0 ){
    marker.color.r = 1.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;
  }
  else{
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
  }
  vis_pub.publish( marker );
}

// Entry point
int main(int argc, char** argv)
{
  // Init the ROS node
  ros::init(argc, argv, "marker");
  ros::NodeHandle nh;
  vis_pub = nh.advertise<visualization_msgs::Marker>( "visualization_marker", 0 );
  
  ros::Rate r(10); // 10 hz
  while (ros::ok())
  {
    ros::spinOnce();
    makeMakrer(0.5,0.5,0.5, 0);
    makeMakrer(0.5,-0.5,0.5, 1);
    r.sleep();
  }  
  return EXIT_SUCCESS;
}

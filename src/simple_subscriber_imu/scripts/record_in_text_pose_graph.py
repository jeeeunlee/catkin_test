#!/usr/bin/env python
import rospy
from nav_msgs.msg import Path

PATH_TOPIC = "/loop_fusion/pose_graph_path"
save_dir = "pose_graph_path.txt"

f = open(save_dir, 'w')

def callback(path_msg):
    graph_length = len(path_msg.poses)
    rospy.loginfo('path_msg callback path length : %d' %(graph_length) )    

    if(graph_length > 330) :        
	f.write('-------------------------')
        for poses_tmp in path_msg.poses :
            t = poses_tmp.header.stamp
            x = poses_tmp.pose.position.x
            y = poses_tmp.pose.position.y
            z = poses_tmp.pose.position.z
            q1 = poses_tmp.pose.orientation.x
            q2 = poses_tmp.pose.orientation.y
            q3 = poses_tmp.pose.orientation.z
            q4 = poses_tmp.pose.orientation.w
            data = "%s, %f, %f, %f, %f, %f, %f, %f \n" %(t, x, y, z, q1, q2, q3, q4) 
            f.write(data)

def listener():
    rospy.loginfo('-----init node')
    rospy.init_node('simple_subscriber_imu',anonymous=True)
    rospy.Subscriber(PATH_TOPIC, Path, callback)
    rospy.spin()
    rospy.loginfo('-----end node')


listener()


f.close()


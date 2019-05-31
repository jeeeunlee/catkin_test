#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu

IMU_TOPIC = "/camera/imu"
save_dir = "test.txt"

#f = open('test.txt', 'w')
f = open(save_dir, 'w')

def callback(imu_msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    t = imu_msg.header.stamp
    dx = imu_msg.linear_acceleration.x
    dy = imu_msg.linear_acceleration.y
    dz = imu_msg.linear_acceleration.z
    rx = imu_msg.angular_velocity.x
    ry = imu_msg.angular_velocity.y
    rz = imu_msg.angular_velocity.z

    data = "%s, %f, %f, %f, %f, %f, %f \n" %(t, dx, dy, dz, rx, ry, rz) 
    f.write(data)
    

def listener():
    rospy.init_node('simple_subscriber_imu',anonymous=True)
    rospy.Subscriber(IMU_TOPIC, Imu, callback)
    rospy.spin()



listener()


f.close()


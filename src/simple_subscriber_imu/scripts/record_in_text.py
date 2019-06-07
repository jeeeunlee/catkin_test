#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu

IMU_TOPIC1 = "/camera/accel/sample"
IMU_TOPIC2 = "/camera/gyro/sample"
save_dir1 = "test2_1.txt"
save_dir2 = "test2_2.txt"

#f = open('test.txt', 'w')
f1 = open(save_dir1, 'w')
f2 = open(save_dir2, 'w')

def callback1(imu_msg1):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    t1 = imu_msg1.header.stamp
    dx = imu_msg1.linear_acceleration.x
    dy = imu_msg1.linear_acceleration.y
    dz = imu_msg1.linear_acceleration.z

    data = "%s, %f, %f, %f \n" %(t1, dx, dy, dz) 
    f1.write(data)
    
def callback2(imu_msg2):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    t2 = imu_msg2.header.stamp
    rx = imu_msg2.angular_velocity.x
    ry = imu_msg2.angular_velocity.y
    rz = imu_msg2.angular_velocity.z

    data = "%s, %f, %f, %f \n" %(t2, rx, ry, rz) 
    f2.write(data)

def listener():
    rospy.init_node('simple_subscriber_imu',anonymous=True)
    rospy.Subscriber(IMU_TOPIC1, Imu, callback1)
    rospy.Subscriber(IMU_TOPIC2, Imu, callback2)
    rospy.spin()



listener()


f1.close()
f2.close()


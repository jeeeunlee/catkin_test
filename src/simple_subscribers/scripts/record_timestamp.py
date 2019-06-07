#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Image

IMU_TOPIC = "/camera/imu"
IMU_TOPIC1 = "/camera/accel/sample"
IMU_TOPIC2 = "/camera/gyro/sample"
IMG_TOPIC1 = "/camera/infra1/image_rect_raw"
IMG_TOPIC2 = "/camera/infra2/image_rect_raw"

save_dir_imu = "test1.txt"
save_dir_imu1 = "test1_1.txt"
save_dir_imu2 = "test1_2.txt"
save_dir_img1 = "test2_1.txt"
save_dir_img2 = "test2_2.txt"

f1 = open(save_dir_imu, 'w')
f1_1 = open(save_dir_imu1, 'w')
f1_2 = open(save_dir_imu2, 'w')

f2_1 = open(save_dir_img1, 'w')
f2_2 = open(save_dir_img2, 'w')

def callback_imu(imu_msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    t_callback = time.time()
    t = imu_msg.header.stamp
    x = imu_msg.linear_acceleration.x
    y = imu_msg.linear_acceleration.y
    z = imu_msg.linear_acceleration.z
    rx = imu_msg.angular_velocity.x
    ry = imu_msg.angular_velocity.y
    rz = imu_msg.angular_velocity.z
    
    data = "%f, %s, %f, %f, %f, %f, %f, %f\n" %(t_callback, t, x,y,z,rx,ry,rz) 
    f1.write(data)

def callback_imu1(imu_msg1):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    t_callback = time.time()
    t = imu_msg1.header.stamp
    data = "%f, %s\n" %(t_callback, t) 
    f1_1.write(data)

def callback_imu2(imu_msg2):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    t_callback = time.time()
    t = imu_msg2.header.stamp
    data = "%f, %s\n" %(t_callback, t) 
    f1_2.write(data)
    
def callback_image1(img_msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    t_callback = time.time()
    t = img_msg.header.stamp
    data = "%f, %s\n" %(t_callback, t)
    f2_1.write(data)

def callback_image2(img_msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    t_callback = time.time()
    t = img_msg.header.stamp
    data = "%f, %s\n" %(t_callback, t) 
    f2_2.write(data)

def listener():
    print("---\n")
    rospy.init_node('simple_subscribers',anonymous=True)
    rospy.Subscriber(IMU_TOPIC, Imu, callback_imu)
    rospy.Subscriber(IMU_TOPIC1, Imu, callback_imu1)
    rospy.Subscriber(IMU_TOPIC2, Imu, callback_imu2)
    rospy.Subscriber(IMG_TOPIC1, Image, callback_image1)
    rospy.Subscriber(IMG_TOPIC2, Image, callback_image2)
    rospy.spin()


listener()

f1.close()
f1_1.close()
f1_2.close()
f2_1.close()
f2_2.close()


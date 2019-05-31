#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

IMG_TOPIC = "/camera/infra1/image_rect_raw"
save_dir = "image.txt"

#f = open('test.txt', 'w')
f = open(save_dir, 'w')

def callback(img_msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    t = img_msg.header.stamp
    data = "%s \n" %(t) 
    f.write(data)
    

def listener():
    rospy.init_node('simple_subscriber_imu',anonymous=True)
    rospy.Subscriber(IMG_TOPIC, Image, callback)
    rospy.spin()


listener()


f.close()


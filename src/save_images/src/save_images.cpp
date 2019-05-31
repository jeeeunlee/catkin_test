#include <stdio.h>
#include <queue>
#include <vector>
#include <thread>
#include <mutex>
#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>

#include <sensor_msgs/Image.h>
#include <eigen3/Eigen/Dense>
#include <opencv2/opencv.hpp>
#include <opencv2/core/eigen.hpp>

using namespace std;
queue<sensor_msgs::ImageConstPtr> img0_buf;
queue<sensor_msgs::ImageConstPtr> img1_buf;
std::mutex m_buf;
int inputImageCnt;
std::string filepath;
int callImageCnt;

void img0_callback(const sensor_msgs::ImageConstPtr &img_msg)
{
    m_buf.lock();
    img0_buf.push(img_msg);
    m_buf.unlock();
}

void img1_callback(const sensor_msgs::ImageConstPtr &img_msg)
{
    m_buf.lock();
    img1_buf.push(img_msg);
    m_buf.unlock();
}

cv::Mat getImageFromMsg(const sensor_msgs::ImageConstPtr &img_msg)
{
    cv_bridge::CvImageConstPtr ptr;
    if (img_msg->encoding == "8UC1")
    {
        sensor_msgs::Image img;
        img.header = img_msg->header;
        img.height = img_msg->height;
        img.width = img_msg->width;
        img.is_bigendian = img_msg->is_bigendian;
        img.step = img_msg->step;
        img.data = img_msg->data;
        img.encoding = "mono8";
        ptr = cv_bridge::toCvCopy(img, sensor_msgs::image_encodings::MONO8);
    }
    else
        ptr = cv_bridge::toCvCopy(img_msg, sensor_msgs::image_encodings::MONO8);

    cv::Mat img = ptr->image.clone();
    return img;
}

void saveImage(double time0, double time1, const cv::Mat &image0, const cv::Mat &image1)
{
    cout << "save image : " << inputImageCnt << "/"<< callImageCnt << endl;
    callImageCnt=0;
    inputImageCnt++;    

    stringstream img0_path, img1_path;
    img0_path<<filepath<<"_left"<< setfill ('0') << std::setw (3) << inputImageCnt<<".jpg";
    img1_path<<filepath<<"_right"<< setfill ('0') << std::setw (3) << inputImageCnt<<".jpg";

    imwrite( img0_path.str(), image0 );
    imwrite( img1_path.str(), image1 );
}


void process()
{
    sensor_msgs::ImageConstPtr image_msg = NULL;

    while(1)
    {        
        cv::Mat image0, image1;
        std_msgs::Header header;
        double time0=0, time1=0;
        m_buf.lock();
        if (!img0_buf.empty() && !img1_buf.empty())
        {
            callImageCnt++;
            time0 = img0_buf.front()->header.stamp.toSec();
            time1 = img1_buf.front()->header.stamp.toSec();
            // 0.003s sync tolerance

            header = img0_buf.front()->header;
            image0 = getImageFromMsg(img0_buf.front());
            img0_buf.pop();
            image1 = getImageFromMsg(img1_buf.front());
            img1_buf.pop();
            // printf("find img0 and img1 buf size = %d, %d\n", img0_buf.size(), img1_buf.size() );            
        }
        m_buf.unlock();

        if(!image0.empty() && callImageCnt>9)
            saveImage(time0, time1, image0, image1);

        chrono::milliseconds dura(1);
        std::this_thread::sleep_for(dura);
    }
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "save_images");
    ros::NodeHandle n("~");

    callImageCnt=0;
    inputImageCnt=0;

    ROS_INFO("init node");

    filepath = argv[1];

    // subscribe topics
    std::string IMAGE0_TOPIC, IMAGE1_TOPIC;
    IMAGE0_TOPIC = "/camera/infra1/image_rect_raw";
    IMAGE1_TOPIC = "/camera/infra2/image_rect_raw";
    ros::Subscriber sub_img0 = n.subscribe(IMAGE0_TOPIC, 200, img0_callback);
    ros::Subscriber sub_img1 = n.subscribe(IMAGE1_TOPIC, 200, img1_callback);

    ROS_INFO("start thread");

    // start image processing thread
    std::thread measurement_process;
    measurement_process = std::thread(process);

    ROS_INFO("start ros spin");

    ros::spin();

    ROS_INFO("end ros spin");

    return 0;
}
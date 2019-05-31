#!/bin/bash 

. $HOME/.bashrc

TERM=$(which gnome-terminal)
echo Using $TERM

function start {
  #gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; pwd; echo $1; $1; echo Exiting..; sleep 1\""
  gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; $1; echo Exiting..; sleep 5\""
}

####################################################################

echo -e "choose the input : 1. realsensor / 2. rosbag play : \c"
read input_option
echo "input_option: $input_option"

if [ $input_option = '2' ];then 
	echo "rosbag playlist : "
	input=`find /home/lee/videoRecord` 
	for i in $input 
	do 
	  echo $i 
	done

	echo -e "play 할 파일을 입력하세요: \c "
	read filepath
	echo "filepath: $filepath"
else
	echo Running now..
	sleep 1
fi

echo -e "run the loopclosure? (y/n) : \c"
read b_loop_closure
echo "b_loop_closure: $b_loop_closure"


####################################################################

## 1. run rviz
sleep 1
start "roslaunch vins vins_rviz.launch"

## 2. run vins estimator
sleep 5
start "rosrun vins vins_node ~/catkin_vins/src/VINS-Fusion/config/realsense_d435i/realsense_stereo_imu_config.yaml"

## 3. run (optional) loop closure
if [ $b_loop_closure = 'y' ];then 
	sleep 3
	start "rosrun loop_fusion loop_fusion_node ~/catkin_vins/src/VINS-Fusion/config/realsense_d435i/realsense_stereo_imu_config.yaml"
fi

## 4. run camera
sleep 3
if [ $input_option = '2' ];then 
	start "rosbag play $filepath"
else
	start "roslaunch realsense2_camera rs_camera_imu.launch "
fi


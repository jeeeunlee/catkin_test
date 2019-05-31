#!/bin/bash 

. $HOME/.bashrc

TERM=$(which gnome-terminal)
echo Using $TERM

function start {
  #gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; pwd; echo $1; $1; echo Exiting..; sleep 1\""
  gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; $1\""
}


#start "rosbag record -o ~/videoRecord/ /camera/imu /camera/infra1/image_rect_raw /camera/infra2/image_rect_raw"
start "rosbag record -o /media/lee/sd/video/ /camera/imu /camera/infra1/image_rect_raw /camera/infra2/image_rect_raw"

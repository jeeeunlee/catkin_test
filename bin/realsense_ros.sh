#!/bin/bash 

. $HOME/.bashrc

TERM=$(which gnome-terminal)
echo Using $TERM

function start {
  #gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; pwd; echo $1; $1; echo Exiting..; sleep 1\""
  gnome-terminal  --command "bash -i -c \". $HOME/.bashrc; $1; echo Exiting..; sleep 3\""
}


start "roslaunch realsense2_camera rs_camera_imu.launch "

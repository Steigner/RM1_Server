#!/bin/bash

echo "Launching application, please wait!"

roslaunch rosbridge_server rosbridge_websocket.launch &
P1=$!

sleep 3
source ~/catkin_ws/devel/setup.bash
rosrun robo_control switch.py &
P2=$!

sleep 2
source ~/catkin_ws/devel/setup.bash
rosrun tf2_web_republisher tf2_web_republisher &
P3=$!

wait $P1 $P2 $P3

sleep 5
killall -9 roscore
killall -9 rosmaster
killall -9 gzserver
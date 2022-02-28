#!/bin/bash

echo "Launching application, please wait!"

roslaunch rosbridge_server rosbridge_websocket.launch &
P1=$!

sleep 2
source ~/catkin_ws/devel/setup.bash
rosrun tf2_web_republisher tf2_web_republisher &
P2=$!

sleep 2
source ~/catkin_ws/devel/setup.bash
rosrun robo_control switch.py &
P3=$!

if [[ $1 != "sim" ]]
then
    sleep 2
    source ~/catkin_ws/devel/setup.bash
    sudo chmod a+rw /dev/ttyACM0
    roslaunch optoforce optoforce.launch &
    P4=$!

    wait $P1 $P2 $P3 $P4
else
    wait $P1 $P2 $P3
fi

sleep 5
killall -9 roscore
killall -9 rosmaster
killall -9 gzserver
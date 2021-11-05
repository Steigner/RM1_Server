#!/bin/bash

echo test

if [[ $1 -eq "sim" ]]
    then 
        source ~/catkin_ws/devel/setup.bash
        roslaunch robo_control run.launch sim:=true &
        P1=$!
        sleep 2

        source ~/catkin_ws/devel/setup.bash
        roslaunch robo_moveit ur3_moveit_planning_execution.launch sim:=true &
        P2=$!

        wait $P1 $P2
        sleep 5

    else 
        source ~/catkin_ws/devel/setup.bash
        roslaunch robo_control run.launch ip_adress:=$1
fi

    <node name="tf2_web_republisher" pkg="tf2_web_republisher" type="tf2_web_republisher"/>
	<include file="$(find robo_control)/launch/show_result.launch"/>

"""
source ~/catkin_ws/devel/setup.bash
rosrun robo_control switch.py &
P2=$!
sleep 2
"""



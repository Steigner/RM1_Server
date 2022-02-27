<p align="center">
  <img src="https://user-images.githubusercontent.com/54715463/155894839-e6a05c2e-aa95-4b53-bb4d-c4cbc1a964b9.png" alt="Material Bread logo">
</p>

***

# RoboMedicinae1 - Server
<a href="https://github.com/Steigner/RM1_server/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
RM1 is an experimental robotic platform created to automate antigen testing. This project was developed as part of a master's thesis. The aim was to create a functional and modular prototype that is easily modifiable and deployable after debugging. The basic idea is to create a web-based server that communicates with ROS. ROS was used in the work as a simulation and debugging environment, mainly for robot control. The thesis is divided into thour main parts:

+ [<=](https://github.com/Steigner/RM1_server) RM1 - Server
+ [<=](https://github.com/Steigner/RM1_ROS) RM1 - ROS         
+ RM1 - Gripper
+ RM1 - Seg. ANN

| Part                       | Software                    |
| -------------------------- | --------------------------- |
| Conteiner                  | Docker-Compose              |
| Package manager            | Poetry                      |
| Back-end                   | Python 3                    |
| Front-end                  | JavaScript, CSS, HTML       |

In this repository there is a Python Flask Server, that takes care of running the kernel on the back-end, one of the curiosities is that the Intel Realsense camera is connected to the server. This is based on the original design, which intended for a local server only and ROS was to be used for robot control. The gripper and force-torque sensor are included in ROS, because the RG2 and Hex-e sensor are connected to the robot.

For a fully functional application, it is necessary to implement both **RM1-Server** and **RM1-ROS** in your operating system. So you can run the simulation and see the application in operation. For real-world application, it is advisable to print the enclosed **RM1-Gripper** models with the fasteners on a 3D printer and assemble them.

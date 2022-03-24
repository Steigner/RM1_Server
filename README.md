<p align="center">
  <img src="https://user-images.githubusercontent.com/54715463/155894839-e6a05c2e-aa95-4b53-bb4d-c4cbc1a964b9.png" alt="Material Bread logo">
</p>

***

# RoboMedicinae1 - Server
<a href="https://github.com/Steigner/RM1_server/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Open-source, copy and modify what you need!**

**Open-source, kopírujte a upravujte co potřebujete!**

## About
RM1 is an experimental robotic platform created to automate antigen testing. This project was developed as part of a master's thesis. The aim was to create a functional and modular prototype that is easily modifiable and deployable after debugging. The basic idea is to create a web-based server that communicates with ROS. ROS was used in the work as a simulation and debugging environment, mainly for robot control. The thesis is divided into four main parts:

+ [<=](https://github.com/Steigner/RM1_server) RM1 - Server
+ [<=](https://github.com/Steigner/RM1_ROS) RM1 - ROS         
+ [<=](https://github.com/Steigner/RM1_Gripper) RM1 - Gripper
+ RM1 - Seg. ANN

In this repository there is a Python Flask Server, that takes care of running the kernel on the back-end, one of the curiosities is that the Intel Realsense camera is connected to the server. This is based on the original design, which intended for a local server only and ROS was to be used for robot control. The gripper and force-torque sensor are controled and included in ROS, because the RG2 and Hex-e sensor are connected to the robot.

For a fully functional application, it is necessary to implement both **RM1-Server** and **RM1-ROS** in your operating system. So you can run the simulation and see the application in operation. For real-world application, it is advisable to print the enclosed **RM1-Gripper** models with the fasteners on a 3D printer and assemble them.

During the design, emphasis was put on modularity, for the benefit of the user it is possible to run the server in Docker-compose or purely in Python, for more information go to the **/app** directory.

**Server software equipment**

| Part                       | Software                    |
| -------------------------- | --------------------------- |
| Conteiner                  | Docker-Compose              |
| Package manager            | Poetry                      |
| Back-end                   | Python 3                    |
| Front-end                  | JavaScript, CSS, HTML       |
| System run                 | Bash                        |

## Functions

* Search patient in database by PIN(Perosnal Identification Number)/Surname or QR code reader with PIN
* Face ID - compare of patient from streaming color image by photo to database
* Face detection - detection of human face landmarks
* Scan face - scan aligned color image to depth and reconstructed 3D point cloud
* Identification of center of nostril - own programmed seg. cnn for nostrils with post processing of centroid
* Manual control of robot - simple UI for control robot joints
* Show point cloud in browser
* Show digital twin in browser
* Get basic data about weather
* Streaming color, depth, infra image 
* Streaming basic data from robot
* Generate PDF document base on HTML input
* Brute force test to crack password
* Basic Python tests
* Pick and place, motion to detected center of nostril 
* Simulation x Real world control of robot

## Screenshots and videos

<p align="center"> <b>Click to full resolution</b> </p>

![image](https://user-images.githubusercontent.com/54715463/155899512-e7d854bb-060b-4e19-be24-600c7cabbe04.png)

![image](https://user-images.githubusercontent.com/54715463/155899679-3afab5fb-2a01-4d45-abb6-263c80247c3f.png)

![image](https://user-images.githubusercontent.com/54715463/155899886-1813599a-59da-47e2-b654-82b5cb793f79.png)

![image](https://user-images.githubusercontent.com/54715463/155900177-90c77f49-8372-4aa7-be7e-21ef67d234d2.png)

![image](https://user-images.githubusercontent.com/54715463/155899981-0969caea-8504-43c1-b695-1da7be42af88.png)

![image](https://user-images.githubusercontent.com/54715463/155900207-175ae7f0-7ab2-4afe-ba4e-03f5a46f3fd7.png)

![image](https://user-images.githubusercontent.com/54715463/155900015-231af3f1-15e2-4520-85c3-ccabb89b4ef5.png)

![patient_data](https://user-images.githubusercontent.com/54715463/160019352-1d882d6d-75cd-4df8-89b8-99d5c110be24.png)

![test](https://user-images.githubusercontent.com/54715463/155900091-78fa76ad-a566-49d8-b847-1ce7e81e3243.jpg)

## Authors

* Author: Martin Juricek
* Designer: Katerina Monsportova
* Supervisor: Roman Parak

## References

[Faculty of Mechanical Engineering BUT](https://www.fme.vutbr.cz/en)

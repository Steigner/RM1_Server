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

+ [<=](https://github.com/Steigner/Robo_Medicinae_I) Robo Medicinae I
+ [<=](https://github.com/Steigner/RM1_server) RM1 - Server
+ [<=](https://github.com/Steigner/RM1_ROS) RM1 - ROS         
+ [<=](https://github.com/Steigner/RM1_Gripper) RM1 - Gripper
+ [<=](https://github.com/Steigner/RM1_SegCNN) RM1 - SegCNN

In this repository there is a Python Flask Server, that takes care of running the kernel on the back-end, one of the curiosities is that the Intel Realsense camera is connected to the server. This is based on the original design, which intended for a local server only and ROS was to be used for robot control. The gripper and force-torque sensor are controled and included in ROS, because the RG2 and Hex-e sensor are connected to the robot.

For a fully functional application, it is necessary to implement both **RM1-Server** and **RM1-ROS** in your operating system. So you can run the simulation and see the application in operation. For real-world application, it is advisable to print the enclosed **RM1-Gripper** models with the fasteners on a 3D printer and assemble them.

During the design, emphasis was put on modularity, for the benefit of the user it is possible to run the server in Docker-Compose or purely in Python, for more information go to the **/app** directory.

**Note:** If there will be a problem with poetry in the **requriements.txt** file there should be a working library configuration.

Supported resolution:

* 1920x1080
* 1280x960

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


## ARM architecture
The solution was tested on a single board computer Nvidia Jetson Xavier Development Kit. This computer is based on ARM architecture while this server was developed on x86 architecture. The alternative of adding Docker Compose for ARM is not currently addressed. The solution has been tested on the Flask development server. Here are some notes on how to get the solution running on ARM:

* Install Python >=3.8
* Do not use Poetry package manager, some libries raise up installation error.
* Install the libraries directly into Python PIP.
* The main problem arises with Intel Realsense. -> It is recommended to build the SDK from source.

Procedure:
1) Download librealsense source as .zip: https://github.com/IntelRealSense/librealsense/releases/
2) After downloading the .zip file, its contents should be extracted so that you have a librealsense folder
3) go to the librealsense root directory

```bash
$ mkdir build && cd build
$ cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=/usr/bin/python3.8
# Note: -DPYTHON_EXECUTABLE=/usr/bin/python3.8 -> path to installed Python
$ make -j4
$ sudo make install
$ export PYTHONPATH=$PYTHONPATH:/home/jetson/Desktop/librealsense-2.50.0/build/wrappers/python
# Note: librealsense-2.50.0 -> depands on version of downloaded version SDK (if you not change name)
$ sudo nano .bashrc
# Note: paste into .bashrc command export PYTHONPATH=$PYTHONPATH:/home/jetson/Desktop/librealsense-2.50.0/build/wrappers/python
```
Source: https://couka.de/2020/10/27/jetson-nano-install-librealsense-with-python-bindings/

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

## Citation
If you want to quote please check the header repository. 

github.com/Steigner/Robo_Medicinae_I [=>](https://github.com/Steigner/Robo_Medicinae_I) 

## References

[Faculty of Mechanical Engineering BUT](https://www.fme.vutbr.cz/en)

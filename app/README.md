# RoboMedicinae1 - Server

## Sign in:
There are signature options in the user database, such as:

**User**
<p> email: email@email.com      | password: heslo</p>
<p> email: author@email.com     | password: heslo</p>

**Admin**
<p> email: supervisor@email.com | password: heslo</p>

## Python Flask

One of option is to run as development server, then go to folder **./flask_server**

## Docker
As mentioned above can be run as a docker. 

**Dependencies:**

* Docker-compose - [url](https://docs.docker.com/)

All in one.
Builds, creates, starts, and attaches to containers for a service:

```console
user@user-pc:~$ docker-compose up
```
Gradually.
Builds containers and run:

```console
user@user-pc:~$ docker-compose build
user@user-pc:~$ docker-compose run
```

## ROS Control

You can run ROS start bash script from this file. Attention: in **./run.sh** change **catkin** workspace. For example:

```bash
source ~/catkin_ws/devel/setup.bash
```
to 

```bash
source ~/catkin_tt/devel/setup.bash
```

For control robot is neccesary to have ROS. More information in [RM1-ROS](https://github.com/Steigner/RM1_ROS).

**Dependencies:**

* ROS Melodic Morenia(Tested) - [url](http://wiki.ros.org/melodic)

Run ROS Back-end as simulation:

```console
user@user-pc:~$ ./run.sh sim
```

Run ROS Back-end as real world:

```console
user@user-pc:~$ ./run.sh
```

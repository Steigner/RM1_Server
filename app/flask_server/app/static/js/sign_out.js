// Script - connect to ROS and quit all
// subprogrammes!

var ros = new ROSLIB.Ros();

ros.connect('ws://localhost:9090');

var pub = new ROSLIB.Topic({
    ros: ros,
    name: '/switch',
    messageType: 'std_msgs/String',
});

var mess = new ROSLIB.Message({
    data: "all",
});

pub.publish(mess);

window.location.href = '/';
import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    var ros = ROS_connect();
    
    var cmdVel = new ROSLIB.Topic({
        ros : ros,
        name : '/switch',
        messageType : 'std_msgs/String'
    });

    var twist = new ROSLIB.Message({
        data: "disconnect"       
    });

    // And finally, publish.
    cmdVel.publish(twist);
    
    // wait on connection, then disconnect!!
    window.setTimeout(function(){  
        window.location.href="/home";
    }, 1000);
});
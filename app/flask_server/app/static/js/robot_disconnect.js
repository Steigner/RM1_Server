import {ROS_connect} from './modules/ROS_connect.js';

$(function() { 
    var ros = ROS_connect();
    var service_disconnect = new ROSLIB.Service({
        ros : ros,
        name : '/disconnect_robot',
        serviceType : 'std_srvs/Trigger'
    });

    service_disconnect.advertise(function(request, response) {
        response['success'] = true;
        response['message'] = "disconnect";
        return true;
    });
    
    // wait on connection, then disconnect!!
    window.setTimeout(function(){  
        window.location.href="/home";
    }, 5000);
});
import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    var ros = ROS_connect();
    
    var menu = new ROSLIB.Topic({
        ros : ros,
        name : '/switch',
        messageType : 'std_msgs/String'
    });

    var init = new ROSLIB.Message({
        data: "nostrill"       
    });

    // And finally, publish.
    menu.publish(init);

    var listener = new ROSLIB.Topic({
        ros : ros,
        name : '/info',
        messageType : 'std_msgs/String'
    });

    listener.subscribe(function(message) {
        console.log('Received message on ' + message.data);
        listener.unsubscribe();
        
        $.ajax({        
            url: '/face_scan',
            type: 'POST',
            data: {value: "point"},
            success: function(response) {
                console.log(response.point);
                
                var point = new ROSLIB.Param({
                    ros : ros,
                    name : 'point'
                });
                
                point.set([response.point[0], response.point[1], response.point[2]]);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
})
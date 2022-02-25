import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    $("#disconnect_button").click(function(){
        $(".loading_background, .loading_label, .wrapper").show();
        
        var ros = ROS_connect();
        
        var info = new ROSLIB.Topic({
            ros : ros,
            name : '/switch',
            messageType : 'std_msgs/String'
        });

        var listener = new ROSLIB.Topic({
            ros : ros,
            name : '/rosout_agg',
            messageType : 'rosgraph_msgs/Log'
        });

        var pub = new ROSLIB.Message({
            data: "disconnect"       
        });

        ros.on('connection', function() {
            console.log("Connected and publishing");
            info.publish(pub);

        
            listener.subscribe(function(message) {
                console.log(message.msg);
                if (message.msg.includes('Controller Spawner error while taking down controllers: transport error completing')) { 
                    window.setTimeout(function(){  
                        $(".loading_background, .loading_label, .wrapper").hide();
                        window.location.href="/home";
                    }, 3000);
                }
            });
        });
    });
});
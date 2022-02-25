import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    $("#test_process").click(function(){
        if (confirm('Robot start test process. Are u sure?')) {
            $(".loading_background, .loading_label, .wrapper").show();

            var ros = ROS_connect();
            var menu = new ROSLIB.Topic({
                ros : ros,
                name : '/switch',
                messageType : 'std_msgs/String'
            });
        
            var init = new ROSLIB.Message({
                data: "init_mot"       
            });
            
            menu.publish(init);
            
            var listener = new ROSLIB.Topic({
                ros : ros,
                name : '/info',
                messageType : 'std_msgs/String'
            });
            
            listener.subscribe(function(message) {
                console.log('Received message on ' + message.data);
                listener.unsubscribe();
                $(".loading_background, .loading_label, .wrapper").hide();
                window.location.href="/menu";
            });
        } else {
            console.log('Nothing go wrong.');
        }
    });

    $("#stream_cam").click(function(){
        window.location.href="/show_cam_stream"
    });

    $("#face_id").click(function() {
        $(".loading_background, .loading_label, .wrapper").show();
        window.location.href="/faceID";
    });
});
import { ROS_connect } from './modules/ROS_connect.js';
import { insert_error_cookie } from './modules/cookies.js';

$(function () {
    $('#dash').hide();

    $('#dash').click(function () {
        window.location.href = '/dash';
    });

    $('#scan').click(function () {
        $('.loading_background, .loading_label, .wrapper').show();
        // AJAX
        // Note:
        //  Start scan face
        $.ajax({
            url: '/face_scan',
            type: 'POST',
            data: { value: 'scan' },
            success: function (response) {
                $('.loading_background, .loading_label, .wrapper').hide();
                if (response == 'Camera is not pluged-in!') {
                    insert_error_cookie(response);
                    window.location.href = '/home';
                }
                if (response == 'ok') {
                    alert(response);
                    // open another option to show point cloud in broswer
                    $('#dash').show();
                }
            },
            error: function (error) {
                console.log(error);
            },
        });
    });

    $('#test').click(function () {
        // $(".loading_background, .loading_label, .wrapper").show();
        
        // ROS NODES
        var ros = ROS_connect();
        
        // switch node
        var menu = new ROSLIB.Topic({
            ros: ros,
            name: '/switch',
            messageType: 'std_msgs/String',
        });

        // message to start motion part to nostril
        var init = new ROSLIB.Message({
            data: 'nostrill',
        });

        menu.publish(init);
        
        // AJAX
        // Note:
        //  Start motion to nostril, before that get point 
        //  of nostril in 3D space
        $.ajax({
            url: '/face_scan',
            type: 'POST',
            data: { value: 'test' },
            success: function (response) {
                if (response == 'nok') {
                    alert('No point!');
                } else {
                    console.log(response.point);

                    var point = new ROSLIB.Param({
                        ros: ros,
                        name: 'point',
                    });

                    point.set([
                        response.point[0],
                        response.point[1],
                        response.point[2],
                    ]);
                }
            },
            error: function (error) {
                console.log(error);
            },
        });
    });
});

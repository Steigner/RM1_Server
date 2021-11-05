import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    $("#up").prop("disabled", true);
    $("#down").prop("disabled", true);
    //$(".back_button").prop("disabled", true);
    $("#face_val.next_button").prop("disabled", true);

    var ros = ROS_connect();
    
    var up_down = new ROSLIB.Topic({
        ros : ros,
        name : '/up_down',
        messageType : 'std_msgs/String'
    });

    var menu = new ROSLIB.Topic({
        ros : ros,
        name : '/switch',
        messageType : 'std_msgs/String'
    });

    var init = new ROSLIB.Message({
        data: "init"       
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
        $("#up").prop("disabled", false);
        $("#down").prop("disabled", false);
        //$(".back_button").prop("disabled", false);
        $("#face_val.next_button").prop("disabled", false);
    });
    
    $("#up").click(function(){
        var data = new ROSLIB.Message({
            data: "up"
        });
        up_down.publish(data);
        return
    });

    $("#down").click(function(){
        var data = new ROSLIB.Message({
            data: "down"
        });
        up_down.publish(data);
        return
    });

    // AJAX
    // Note:
    //  If click on back button stop streaming -> garbage collector.
    $(".back_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/face_position',
            type: 'POST',
            data: {value: "stop_det_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/con_pan";
        }, 300);
    });

    // AJAX
    // Note:
    //  If click on next button stop streaming -> garbage collector.
    $("#face_val.next_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/face_position',
            type: 'POST',
            data: {value: "stop_det_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/face_scan";
        }, 3000);
    });

    // AJAX
    // Note:
    //  Start streaming video on response url.
    $.ajax({        
        url: '/face_position',
        type: 'POST',
        data: {value: "position"},
        success: function(response) {     
            $('.stream').attr("src", response.url);
        },
        error: function(error) {
            console.log(error);
        }
    });
})
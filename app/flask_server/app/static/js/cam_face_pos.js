import { ROS_connect } from './modules/ROS_connect.js';
import { insert_error_cookie, allert } from './modules/cookies.js';

function anim() {
    let animation = anime({
        targets: '.image',
        borderRadius: '35%',
        duration: 800,
        easing: 'linear',
        direction: 'alternate',
        loop: true,
    });
    return animation;
}

function disable() {
    $('#face_val.next_button').prop('disabled', true);
    $('.back_button').prop('disabled', true);
    $('#up').prop('disabled', true);
    $('#down').prop('disabled', true);
}

function undisable() {
    $('#face_val.next_button').prop('disabled', false);
    $('.back_button').prop('disabled', false);
    $('#up').prop('disabled', false);
    $('#down').prop('disabled', false);
}

$(function () {
    disable();
    let animation = anim();
    
    // ROS NODES
    var ros = ROS_connect();

    // up down node
    var up_down = new ROSLIB.Topic({
        ros: ros,
        name: '/up_down',
        messageType: 'std_msgs/String',
    });

    // switch node
    var menu = new ROSLIB.Topic({
        ros: ros,
        name: '/switch',
        messageType: 'std_msgs/String',
    });

    // message run rotate part of motion script
    var init = new ROSLIB.Message({
        data: 'rotate_mot',
    });

    // AJAX
    // Note:
    //  Start streaming video on response url.
    $.ajax({
        url: '/face_position',
        type: 'POST',
        data: { value: 'position' },
        success: function (response) {
            if (response == 'Camera is not pluged-in!') {
                insert_error_cookie(response);
                window.location.href = '/home';
            } else {
                animation.restart();
                animation.pause();
                $('.stream').attr('src', response.url);
                undisable();
                menu.publish(init);

                var listener = new ROSLIB.Topic({
                    ros: ros,
                    name: '/info',
                    messageType: 'std_msgs/String',
                });

                listener.subscribe(function (message) {
                    console.log('Received message on ' + message.data);
                    listener.unsubscribe();
                    $('#up').prop('disabled', false);
                    $('#down').prop('disabled', false);
                    //$(".back_button").prop("disabled", false);
                    $('#face_val.next_button').prop('disabled', false);
                });
            }
        },
        error: function (error) {
            console.log(error);
        },
    });

    $('#up').click(function () {
        var data = new ROSLIB.Message({
            data: 'up',
        });
        up_down.publish(data);
        return;
    });

    $('#down').click(function () {
        var data = new ROSLIB.Message({
            data: 'down',
        });
        up_down.publish(data);
        return;
    });

    // AJAX
    // Note:
    //  If click on back button stop streaming -> garbage collector.
    $('.back_button').click(function () {
        $('.stream').off();
        $('.stream').removeAttr('src');

        var init = new ROSLIB.Message({
            data: 'rotate_mot_stop',
        });

        menu.publish(init);

        $.ajax({
            url: '/face_position',
            type: 'POST',
            data: { value: 'stop_det_cam' },
            error: function (error) {
                console.log(error);
            },
        });
        setTimeout(function () {
            window.location.href = '/con_pan';
        }, 300);
    });

    // AJAX
    // Note:
    //  If click on next button stop streaming -> garbage collector.
    $('#face_val.next_button').click(function () {
        $('.stream').off();
        $('.stream').removeAttr('src');

        var init = new ROSLIB.Message({
            data: 'rotate_mot_stop',
        });

        menu.publish(init);

        $.ajax({
            url: '/face_position',
            type: 'POST',
            data: { value: 'stop_det_cam' },
            error: function (error) {
                console.log(error);
            },
        });

        setTimeout(function () {
            window.location.href = '/face_scan';
        }, 3000);
    });
});

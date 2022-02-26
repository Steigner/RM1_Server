import { Size } from './modules/size.js';
import { ROS_connect } from './modules/ROS_connect.js';

$(function () {
    var [e1, e2, e3, height_devisor] = Size();

    var dist = 100 / height_devisor;
    var plus_dist = '+=' + dist + 'px';
    var minus_dist = '-=' + dist + 'px';

    var dp_width = $('#numerical.dragable_place').width();
    var dp_height = 100 / height_devisor;

    /**
     * Prepare all elements, for interaction
     * in animations, dragable functions, and so on.
     */

    // hide scrollbar
    document.body.style.overflow = 'hidden';

    // counter for clicks on keyboard_logo
    var counter = 0;

    // find the element that you want to drag.
    var box = document.getElementById('con_rob');

    /* listen to the touchMove event,
    every time it fires, grab the location
    of touch and assign it to box */
    box.addEventListener('touchmove', function (e) {
        // grab the location of touch
        var touchLocation = e.targetTouches[0];

        // assign box new coordinates based on the touch.
        box.style.left = touchLocation.pageX - dp_width + 'px';
        box.style.top = touchLocation.pageY - dp_height + 'px';

        e.preventDefault();
    });

    /* record the position of the touch
    when released using touchend event.
    This will be the drop position. */
    box.addEventListener('touchend', function (e) {
        // current box position.
        var x = parseInt(box.style.left);
        var y = parseInt(box.style.top);
    });

    $('.simple-keyboard').hide();

    // after click on keyboard_logo, we use jquery simple animation function to move defined
    // elemetns up if is counter == 1, if not so second click on keyboard_logo, we use inverted function
    $(document.body).on('click', '.keyboard_logo', function () {
        counter = counter + 1;

        if (counter == 1) {
            $('.title').animate({
                marginTop: minus_dist,
            });

            $('.ip').animate({
                marginTop: minus_dist,
            });

            $('#connect_button').animate({
                marginTop: minus_dist,
            });

            // show hide virtual keyboard with animation rool up
            $('.simple-keyboard').hide().show('slide', { direction: 'down' });
        } else {
            $('.title').animate({
                marginTop: plus_dist,
            });

            $('.ip').animate({
                marginTop: plus_dist,
            });

            $('#connect_button').animate({
                marginTop: plus_dist,
            });

            // hide showed virtual keyboard with animation rool down
            $('.simple-keyboard').hide('slide', { direction: 'down' });

            counter = 0;
        }
    });

    $('#connect_button').click(function () {
        var value = $('.ip_input').val();
        // test if input has ip adress format
        if (
            /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(
                value
            )
        ) {
            // AJAX
            // Note:
            //  post robot connect process
            $.ajax({
                url: '/robot_connect',
                type: 'POST',
                async: true,
                data: { value: value },
            });

            $('.loading_background, .loading_label, .wrapper').show();

            window.setTimeout(function () {
                // connect to ROS
                var ros = ROS_connect();

                // twist change!!
                var cmdVel = new ROSLIB.Topic({
                    ros: ros,
                    name: '/switch',
                    messageType: 'std_msgs/String',
                });

                var twist = new ROSLIB.Message({
                    data: value,
                });
                
                // on connection start listening
                ros.on('connection', function () {
                    console.log('Connected and publishing');
                    cmdVel.publish(twist);

                    var listener = new ROSLIB.Topic({
                        ros: ros,
                        name: '/rosout_agg',
                        messageType: 'rosgraph_msgs/Log',
                    });
                    
                    listener.subscribe(function (message) {
                        console.log(message.msg);
                        
                        // if ROS is connected to robot
                        if (message.msg.includes('Robot mode is now RUNNING')) {
                            $.ajax({
                                url: '/play_button',
                                type: 'POST',
                                async: true,
                            });

                            window.setTimeout(function () {
                                
                                $(
                                    '.loading_background, .loading_label, .wrapper'
                                ).hide();
                                alert(
                                    'Be careful, the process will begin! Robot starts to move.'
                                );
                                $(
                                    '.loading_background, .loading_label, .wrapper'
                                ).show();
                                
                                var ros = ROS_connect();
                                // start init motion
                                var menu = new ROSLIB.Topic({
                                    ros: ros,
                                    name: '/switch',
                                    messageType: 'std_msgs/String',
                                });

                                var init = new ROSLIB.Message({
                                    data: 'init_mot',
                                });

                                menu.publish(init);

                                var listener = new ROSLIB.Topic({
                                    ros: ros,
                                    name: '/info',
                                    messageType: 'std_msgs/String',
                                });
                                
                                // listen if is motion done
                                listener.subscribe(function (message) {
                                    alert('Prepare for patient!');
                                    listener.unsubscribe();
                                    $(
                                        '.loading_background, .loading_label, .wrapper'
                                    ).hide();
                                        
                                    var init = new ROSLIB.Message({
                                        data: 'init_mot_kill',
                                    });
    
                                    menu.publish(init);

                                    window.location.href = '/home';
                                });
                            }, 3000);
                        } else if (
                            message.msg.includes(
                                'MoveGroup context initialization complete'
                            )
                        ) {
                            window.setTimeout(function () {
                                $(
                                    '.loading_background, .loading_label, .wrapper'
                                ).hide();
                                alert(
                                    'Be careful, the process will begin! Robot starts to move.'
                                );
                                $(
                                    '.loading_background, .loading_label, .wrapper'
                                ).show();

                                var menu = new ROSLIB.Topic({
                                    ros: ros,
                                    name: '/switch',
                                    messageType: 'std_msgs/String',
                                });

                                var init = new ROSLIB.Message({
                                    data: 'init_mot',
                                });

                                menu.publish(init);

                                var listener = new ROSLIB.Topic({
                                    ros: ros,
                                    name: '/info',
                                    messageType: 'std_msgs/String',
                                });

                                // listen if is motion done
                                listener.subscribe(function (message) {
                                alert('Prepare for patient!');
                                listener.unsubscribe();
                                $(
                                    '.loading_background, .loading_label, .wrapper'
                                ).hide();
                                var init = new ROSLIB.Message({
                                    data: 'init_mot_kill',
                                });

                                menu.publish(init);

                                window.location.href = '/home';
                                });
                            }, 3000);
                        }
                    });
                });
            }, 2000);
        } else {
            alert('U dont put valid IP adress!!');
        }
    });
});

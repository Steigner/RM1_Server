import {Size} from './modules/size.js';
import {ROS_connect} from './modules/ROS_connect.js';

$(function() { 
    var [e1, e2, e3, height_devisor] = Size()

    var dist = (100/height_devisor);
    var plus_dist = '+=' + dist + "px"
    var minus_dist = '-=' + dist + "px"

    /**
     * Prepare all elements, for interaction
     * in animations, dragable functions, and so on.  
    */

    // counter for clicks on keyboard_logo
    var counter = 0;

    $('.simple-keyboard').hide();

    // need to be first defined elemet, which will be draggable
    $('.simple-keyboard').draggable({});

    // this prevented move with virtual keybouard out from screen resolution
    $('.simple-keyboard').draggable("option", "scroll", false);

    // disable, becouse after holding *.dragable_place* area, we enable it again. 
    $('.simple-keyboard').draggable("disable")

    // after click on keyboard_logo, we use jquery simple animation function to move defined 
    // elemetns up if is counter == 1, if not so second click on keyboard_logo, we use inverted function
    $(document.body).on('click', '.keyboard_logo', function () {  
    
        counter = counter + 1;
        
        if (counter == 1){
            $(".title").animate({ 
                marginTop : minus_dist,
            });
            
            $(".ip").animate({ 
                marginTop : minus_dist,
            });
            
            $("#connect_button").animate({ 
                marginTop : minus_dist,
            });
            
            // show hide virtual keyboard with animation rool up
            $(".simple-keyboard").hide().show("slide", { direction: "down" });
        }

        else{
            $(".title").animate({ 
                marginTop: plus_dist,
            });
            
            $(".ip").animate({ 
                marginTop: plus_dist,
            });
            
            $("#connect_button").animate({ 
                marginTop: plus_dist,
            });
            
            // hide showed virtual keyboard with animation rool down
            $(".simple-keyboard").hide("slide", { direction: "down" });
            
            counter = 0;
        }
    });

    /*-----------------------------------------------------------------*/
    
    $('#connect_button').click(function(){
        var value = $('.ip_input').val();

        if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(value)) {  
            $.ajax({
                url: '/robot_connect',
                type: 'POST',
                data: {value: value},
            });
            
            $(".loading_background, .loading_label, .wrapper").show();

            window.setTimeout(function(){   
                var ros = ROS_connect();
                
                /* ROS SERVICE !! */
                var service_connect = new ROSLIB.Service({
                    ros : ros,
                    name : '/connect_robot',
                    serviceType : 'std_srvs/Trigger'
                });
            
                // Use the advertise() method to indicate that we want to provide this service
                service_connect.advertise(function(request, response) {
                    response['success'] = true;
                    response['message'] = value;
                    return true;
                });

                var listener = new ROSLIB.Topic({
                    ros : ros,
                    name : '/rosout_agg',
                    messageType : 'rosgraph_msgs/Log'
                });
    
                listener.subscribe(function(message) {
                    console.log(message.msg)
                    
                    if (message.msg.includes('Robot mode is now RUNNING')) { 
                        
                        $.ajax({
                            url: '/play_button',
                            type: 'POST',
                        });
                        
                        window.setTimeout(function(){  
                            $(".loading_background, .loading_label, .wrapper").hide();
                            window.location.href="/home";
                        }, 3000);
                    }
                
                });
                
            }, 2000);

        }
        
        else{
            alert("U dont put valid IP adress!!")
        }           
    });

});

$(function() {
    $('.dragable_place').on('mousedown touchstart', function(e) {
        $( ".simple-keyboard" ).draggable("enable");
    })
}).bind('mouseup mouseleave touchend', function() {
    $('.simple-keyboard').draggable("disable")
})

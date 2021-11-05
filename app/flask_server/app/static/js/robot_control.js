// script -> ros connection
import {ROS_connect} from './modules/ROS_connect.js';

/* REDAME: on this file is neccesary to run action_sub.py file
    no private methods for better acces to methods
*/
// EXCEPTIONS!!

class RobotControl{
    constructor(ros){
        this.ros = ros;
        this.timeOut = 0;
        this.count = 0;
    }

    // public method:
    //   input: none
    //   return none
    // Note: In this method we defined topics and parametres for communication
    // with ROS websocket server, which control robot.
    rosnode_init(){  
        // ROS NODES
        // emergency stop node
        this.stop = new ROSLIB.Topic({
            ros : this.ros,
            name : '/switch',
            messageType : 'std_msgs/String'
        });

        // init current position node
        this.cartesian_data = new ROSLIB.Topic({
            ros : this.ros,
            name : '/current_position',
            messageType : 'geometry_msgs/PoseStamped'
        })
        
        // init joint states node
        this.get_data_joint = new ROSLIB.Topic({
            ros : this.ros,
            name : '/joint_states',
            messageType : 'sensor_msgs/JointState'
        })
        
        // init joint action data
        this.joint_act = new ROSLIB.Topic({
            ros : this.ros,
            name : '/action_joint_data',
            messageType : 'sensor_msgs/JointState'
        })

        // init feedback from moveit
        this.status_topic = new ROSLIB.Topic({
            ros : this.ros,
            name : '/move_group/feedback',
            messageType : 'moveit_msgs/MoveGroupActionFeedback'
        })

        // need to be declared as Float32 -> Number()
        // init control velocity node
        this.vel_acc_pub = new ROSLIB.Topic({
            ros : this.ros,
            name : '/set_vel_acc',
            messageType : 'std_msgs/Float32'
        });    
    }

    // public method:
    //   input: none
    //   return none
    // Note: Set up velocity by slider + animation of slider with his level
    velocity_control(){
        var vel_acc_pub = this.vel_acc_pub;

        $('#vel.slider').rangeslider({
            polyfill: false,

            onSlideEnd: function(position, value) {
                $("#value.vel_label").text( value + " %" );

                var move_sett = new ROSLIB.Message({
                    // must be Number
                    data: Number(this.value),
                });
    
                vel_acc_pub.publish(move_sett);
                return 
            }
        })
    }

    // public method:
    //   input: none
    //   return none
    // Note: Feeding data to labels about actual TCP position.
    // Also fast calculator from quaternion to euler.
    data_feed(){
        var cartesian_data = this.cartesian_data;
        
        cartesian_data.subscribe(function(message){  
            //console.log(message.transforms[0].transform.translation.x)
            // cartesian position
            $("#x").text( Math.round(message.pose.position.x*100) + " cm" );
            $("#y").text( Math.round(message.pose.position.y*100) + " cm" );
            $("#z").text( Math.round(message.pose.position.z*100) + " cm" );
            
            var q0 = message.pose.orientation.x;
            var q1 = message.pose.orientation.y;
            var q2 = message.pose.orientation.z;
            var q3 = message.pose.orientation.w;
            
            // method currying -> function inside method
            function quaternion_to_euler(q0,q1,q2,q3){
                var x_rx = 1 - 2*(q1**2 + q2**2);
                var y_rx = 2*(q0*q1 + q2*q3);
                var RX =  Math.atan2(y_rx,x_rx);
        
                var x_ry = 2*(q0*q2 - q3*q1);
                var RY = Math.asin(x_ry);
        
                var y_rz = 2*(q0*q3 + q1*q2);
                var x_rz = 1 - 2*(q2**2 + q3**2)
                var RZ = Math.atan2(x_rz,y_rz);
                
                // euler position
                $("#RX").text( Math.round(RX*(180/Math.PI)) + " °" );
                $("#RY").text( Math.round(RY*(180/Math.PI)) + " °" );
                $("#RZ").text( Math.round(RZ*(180/Math.PI)) + " °" );
            }

            quaternion_to_euler(q0,q1,q2,q3);

        })

        var get_data_joint = this.get_data_joint;
        
        // get joint position of each motor
        get_data_joint.subscribe(function(message){  
            var elbow = message.position[0] * (180/Math.PI);
            var shoulder = message.position[1] * (180/Math.PI);    
            var base = message.position[2] * (180/Math.PI);
            var wrist_1 = message.position[3] * (180/Math.PI);
            var wrist_2 = message.position[4] * (180/Math.PI);
            var wrist_3 = message.position[5] * (180/Math.PI);
            
            $("#base.slider").val(base).change();
            $("#shoulder.slider").val(shoulder).change();
            $("#elbow.slider").val(elbow).change();
            $("#wrist_1.slider").val(wrist_1).change();
            $("#wrist_2.slider").val(wrist_2).change();
            $("#wrist_3.slider").val(wrist_3).change();

            $("#base.joint_label").text( Math.round(base) + " °" );
            $("#shoulder.joint_label").text( Math.round(shoulder) +" °" );
            $("#elbow.joint_label").text( Math.round(elbow) + " °" );
            $("#wrist_1.joint_label").text( Math.round(wrist_1) + " °" );
            $("#wrist_2.joint_label").text( Math.round(wrist_2) +" °" );
            $("#wrist_3.joint_label").text( Math.round(wrist_3) + " °" );
        })
    }

    robot_status(){
        var status_topic = this.status_topic;
        var get_data_joint = this.get_data_joint;
        
        var count = 0;
        
        status_topic.subscribe(function(message){ 
            var status = message.status.status;
            
            if (status == 3 || status == 4){

                count += 1;
                
                if(count == 1){
                    // if status 4 -> error!!
                    // $('input[type="range"]').prop("disabled", false);
                    get_data_joint.subscribe();
                    $('.rangeslider__handle').css("visibility","visible");
                    $('.right, .left').css("visibility","visible");
                    //alert("Pohyb byl proveden!");
                    return
                }
                else{
                    count = 0;
                };
            }
            else{
                return
            };
        });
    }

    // public method:
    //   input: none
    //   return none
    // Note: there we checking status from move group, if it done or in proceses etc ...
    on_slider(slider){
        var joint_act = this.joint_act;
        var get_data_joint = this.get_data_joint;

        $(slider + '.slider').rangeslider({
            polyfill: false,

            onSlide: function(position, value) {
                get_data_joint.unsubscribe();
            },

            onSlideEnd: function(position, value) {
                var joint = new ROSLIB.Message({
                    name : [slider],
                    position:[value * (Math.PI/180)]
                });
                $('.rangeslider__handle').css("visibility","hidden");
                $('.right, .left').css("visibility","hidden");
                joint_act.publish(joint);
                return
            }
        });
    }

    // public method:
    //   input: defined left button
    //   return none
    // Note: if is touch on button stop subscribing and start move to left,
    // then start subscribe again
    on_left(left){
        var get_data_joint = this.get_data_joint
        var joint_act = this.joint_act;

        $(left + '.left').on('touchend mousedown', function() {
            get_data_joint.unsubscribe();
            
            var i = Number($(left+'.slider').val());
            
            // get value from position of slider -> find as more easy way      

            i = i - 5;

            var joint = new ROSLIB.Message({
                name : [left, "no_wait"],
                position:[i * (Math.PI/180)]
            });

            joint_act.publish(joint);

            setTimeout(function(){
                get_data_joint.subscribe();
                $(left + ".joint_label").text( Math.round(i) + " °" );
            }, 200);
        });      
    }

    // public method:
    //   input: defined right button
    //   return none
    // Note: if is touch on button, stop subscribing and start move to right, 
    // then start subscribing again
    on_right(right){
        var get_data_joint = this.get_data_joint
        var joint_act = this.joint_act;

        $(right + '.right').on('touchend mousedown', function() {
            get_data_joint.unsubscribe();
            
            var i = Number($(right+'.slider').val());
            
            // get value from position of slider -> find as more easy way      

            i = i + 5;

            var joint = new ROSLIB.Message({
                name : [right, "no_wait"],
                position:[i * (Math.PI/180)]
            });

            joint_act.publish(joint);

            setTimeout(function(){
                get_data_joint.subscribe();
                $(right + ".joint_label").text( Math.round(i) + " °" );
            }, 200); 
        });      
    }

    // =============================
    // IN PROGRESS
    emergency_stop(){
        var data = new ROSLIB.Message({
            data: "emergency_stop"       
        });
    
        this.stop.publish(data);

        alert("EMERGENCY BUTTON WAS PRESSED");
    }

    // public method:
    //   input: none
    //   return none
    // Note: MAIN
    main(){
        this.rosnode_init();
        this.data_feed();
        this.velocity_control();

        // get all joints of robot
        var elements = ['#base','#shoulder', '#elbow', '#wrist_1', '#wrist_2', '#wrist_3'];
        
        for (var element of elements) {
            this.on_slider(element);
            this.on_right(element);
            this.on_left(element);
        }

        this.robot_status();
    }
}

// MAIN FUNCTION
$(function() {
    var ros = ROS_connect();

    let robot = new RobotControl(ros);

    robot.main();
    
    $(".emergency_stop").click(function() {
        robot.emergency_stop();
    });

    // prevent to open dialog windwo of touch 
    window.oncontextmenu = function(event) {
        event.preventDefault();
        event.stopPropagation();
        return false;
   };
})
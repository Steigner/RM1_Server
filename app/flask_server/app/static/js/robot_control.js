// script -> ros connection
import {ROS_connect} from './modules/ROS_connect.js';

// script -> size devisor
import {Size} from './modules/size.js';

/* REDAME: on this file is neccesary to run action_sub.py file
    no private methods for better acces to methods
*/
// EXCEPTIONS!!

class RobotControl{
    constructor(ros, width_devisor){
        this.ros = ros;
        this.width_devisor = width_devisor;
        this.timeOut = 0;
    }

    // public method:
    //   input: none
    //   return none
    // Note: In this method we defined topics and parametres for communication
    // with ROS websocket server, which control robot.
    rosnode_init(){ 
        // ROS PARAM 
        this.stop = new ROSLIB.Param({
            ros : this.ros,
            name : 'emergency_stop'
        });

        // ROS NODES
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
        var width_devisor = this.width_devisor;

        $("#vel.slider").on('input', function() {
            var val = (2/width_devisor) * this.value;
            $(".vel_level").css({"width": val + "px"});
        });

        $('#vel.slider').on('change', function() {
            
            $("#value.vel_label").text( this.value + " %" );

            var move_sett = new ROSLIB.Message({
                // must be Number
                data: Number(this.value),
            });

            vel_acc_pub.publish(move_sett);

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

            $("#base.slider").val(base);
            $("#shoulder.slider").val(shoulder);
            $("#elbow.slider").val(elbow);
            $("#wrist_1.slider").val(wrist_1);
            $("#wrist_2.slider").val(wrist_2);
            $("#wrist_3.slider").val(wrist_3);
    
            $("#base.joint_label").text( Math.round(base) + " °" );
            $("#shoulder.joint_label").text( Math.round(shoulder) +" °" );
            $("#elbow.joint_label").text( Math.round(elbow) + " °" );
            $("#wrist_1.joint_label").text( Math.round(wrist_1) + " °" );
            $("#wrist_2.joint_label").text( Math.round(wrist_2) +" °" );
            $("#wrist_3.joint_label").text( Math.round(wrist_3) + " °" );
        })
    }

    // public method:
    //   input: none
    //   return none
    // Note: there we checking status from move group, if it done or in proceses etc ...
    rosnode_status(){
        var status_topic = this.status_topic

        status_topic.subscribe(function(message){ 
            var status = message.status.status

            if (status == 3 || status == 4){
                // if status 4 -> error!!
                $(".slider").prop("disabled", false);
            }

            else{
                $(".slider").prop("disabled", true);
            }
            
        })

    }

    // public method:
    //   input: slider
    //   return none
    // Note: if is touch on slider we stop subscribe data on take of we start subscribe again
    on_input(slider){
        var get_data_joint = this.get_data_joint

        $(slider + '.slider').on('mousedown touchstart', function() {            
            get_data_joint.unsubscribe();

        }).bind('mouseup mouseleave touchend', function(){
            get_data_joint.subscribe();
        
        })
    }

    // public method:
    //   input: slider
    //   return none
    // Note: if is touch on slider we stop subscribe data on take of we start subscribe again
    on_change(slider){
        // import rosnode status, which there we subscribe stutus
        this.rosnode_status();
        
        // for publishing -> action_sub.py
        var joint_act = this.joint_act;
        
        $(slider + '.slider').on('change', function() {
                  
            var joint = new ROSLIB.Message({
                name : [slider],
                position:[this.value * (Math.PI/180)]
            });

            joint_act.publish(joint);

        })
    }

    // public method:
    //   input: defined left button
    //   return none
    // Note: if is touch on button stop subscribing and start move to left,
    // then start subscribe again
    on_left(left){
        var get_data_joint = this.get_data_joint

        var joint_act = this.joint_act;

        $(left + '.left').on('mousedown touchstart', function() {
            $(this).addClass('active');

            // get value from position of slider -> find as more easy way 
            var i = Number($(left+'.slider').val());
            
            this.timeOut = setInterval(function(){

                get_data_joint.unsubscribe();
                
                i = i - 0.5;

                $(left + ".joint_label").text( Math.round(i) + " °" );
                
                var joint = new ROSLIB.Message({
                    name : [left, "no_wait"],
                    position:[i * (Math.PI/180)]
                });

                joint_act.publish(joint);
    
            }, 100);
    
        }).bind('mouseup mouseleave touchend', function() {
            $(this).removeClass('active');
            clearInterval(this.timeOut);
            get_data_joint.subscribe();
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

        $(right + '.right').on('mousedown touchstart', function() {
            $(this).addClass('active');

            var i = Number($(right +'.slider').val());
            
            this.timeOut = setInterval(function(){

                get_data_joint.unsubscribe();
                
                i += 0.5;

                $(right + ".joint_label").text( Math.round(i) + " °" );

                var joint = new ROSLIB.Message({
                    name : [right, "no_wait"],
                    position:[i * (Math.PI/180)]
                });

                joint_act.publish(joint);
    
            }, 100);
    
        }).bind('mouseup mouseleave touchend', function() {
            $(this).removeClass('active');
            clearInterval(this.timeOut);
            get_data_joint.subscribe();
        });
    }

    // =============================
    // IN PROGRESS
    emergency_stop(){
        // send signal 0 as STOP
        this.stop.set(0);
        // send signal 100 as NO STOP
        this.stop.set(100);
        alert("EMERGENCY BUTTON WAS PRESSED");
    }

    // public method:
    //   input: none
    //   return none
    // Note: MAIN
    main(){
        this.rosnode_init()
        this.data_feed()
        this.velocity_control()

        // get all joints of robot
        var elements = ['#base','#shoulder', '#elbow', '#wrist_1', '#wrist_2', '#wrist_3']
        
        for (var element of elements) {
            this.on_input(element);
            this.on_change(element);
            this.on_right(element);
            this.on_left(element);
        }
    }
}

// MAIN FUNCTION
$(function() {
    var ros = ROS_connect();
    var [e1, e2, width_devisor, e3] = Size()

    let robot = new RobotControl(ros, width_devisor);

    robot.main();

    $(".emergency_stop").click(function() {
        robot.emergency_stop();
    })
})
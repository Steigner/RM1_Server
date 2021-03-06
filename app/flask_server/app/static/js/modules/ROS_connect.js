// get the ip address from the rosbridge
function get_ip() {
    var ip_adress = 'ws://localhost:9090';

    $.ajax({
        url: '/ip_adress',
        type: 'POST',
        data: { value: 'ip' },
        success: function (response) {
            ip_adress = String('ws://' + response);
        },
        error: function (error) {
            console.log(error);
        },
        // due to global variable ip adress
        async: false,
    });

    return ip_adress;
}

// connect to ros
export function ROS_connect() {
    var ros = new ROSLIB.Ros();

    // get ip adress from server where is ROS bridge
    // WARNING IN deploy use var ip!!
    var ip = get_ip();

    // First, we need to connect to our ROS bridge server setup earlier with the same port number.
    // there is var ip
    //ros.connect('ws://localhost:9090');

    ros.connect(ip + ':9090');

    ros.on('connection', function () {
        console.log('We are connected!');
    });
    ros.on('close', function () {
        console.log('Connection closed.');
    });
    ros.on('error', function (error) {
        console.log(error);
    });

    return ros;
}

import { Size } from './modules/size.js';
import { ROS_connect } from './modules/ROS_connect.js';

$(function init() {
    var [e1, e2, width_devisor, height_devisor] = Size();

    var ros = ROS_connect();

    var viewer = new ROS3D.Viewer({
        divID: 'urdf',
        width: 400 / width_devisor,
        height: 350 / height_devisor,
        background: '#F2F2F2',
        intensity: 1.6,
        antialias: true,
        cameraPose: { x: 0.7, y: 0.7, z: 0.7 },
    });

    var tfClient = new ROSLIB.TFClient({
        ros: ros,
        //fixedFrame : 'world',
        angularThres: 0.001,
        transThres: 0.001,
        rate: 144,
    });

    var urdfClient = new ROS3D.UrdfClient({
        ros: ros,
        tfClient: tfClient,
        path: './static',
        rootObject: viewer.scene,
    });
});

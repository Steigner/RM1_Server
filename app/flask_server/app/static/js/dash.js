import {ROS_connect} from './modules/ROS_connect.js';

$(function() {
    setTimeout(function(){$(".loading_background, .loading_label, .wrapper").show()},100);
    $.ajax({        
        url: '/dash',
        type: 'POST',
        
        success: function(response) {  
            /* possible sending point cloud to ROS
            var points = [];

            console.log();

            for (let i = 0; i < response.x.length; i++) {
                const dict = {x : response.x[i], y : response.y[i], z : response.z[i]}
                points.push(dict);
            };

            var ros = ROS_connect();

            var pcd = new ROSLIB.Topic({
                ros : ros,
                name : '/pcd',
                messageType : 'sensor_msgs/PointCloud'
            });

            var data = new ROSLIB.Message(
            {
                header: {frame_id : "map"},
                points: points,               
            },
            
            );

            pcd.publish(data);
            */

            // Define Data
            var data1 = {
                x: response.x,
                y: response.y,
                z: response.z,
                mode: "markers",
                type: "scatter3d",
                marker: {
                    color: response.c,
                    size: 1
                }
            };
        
            var data2 = {
                
                //x: [response.nz],
                //y: [- response.ny],
                //z: [- response.nz],
                
                x: response.nx,
                y: response.ny,
                z: response.nz,

                mode: "markers",
                type: "scatter3d",
                marker: {
                    color: "red",
                    size: 1
                }
            };
            
            var datal = [data1,data2];

            var layout = {
                scene: {
                    xaxis: {
                        'visible': false,
                        'showgrid': false,
                        'showticklabels': false,
                        'zeroline': false,
                    },

                    yaxis: {
                        'visible': false,
                        'showgrid': false,
                        'showticklabels': false,
                        'zeroline': false,
                    },

                    zaxis: {
                        'visible': false,
                        'showgrid': false,
                        'showticklabels': false,
                        'zeroline': false,
                    },
                },

                margin: {
                    l: 0,
                    r: 0,
                    b: 0,
                    t: 0
                },

                modebar: {
                    'orientation': 'v',
                    'bgcolor': 'rgba(242, 242, 242, 1)',
                    'color': 'rgb(33, 105, 124)',
                    'scale': 10
                },

                paper_bgcolor: 'rgba(0,0,0,0)',
            };
            
            
            Plotly.newPlot("point_cloud", datal, layout, {displayModeBar: true}).then(function() { 
                $(".loading_background, .loading_label, .wrapper").hide();
            });
            

            /*
            // get point -> move to defined point !!
            var myPlot = document.getElementById('point_cloud');
            myPlot.on('plotly_click', function(data){
                alert(data.points[0].x + " = x")
                //console.log(data.points[0].x, data.points[0].y, data.points[0].z);
            });
            */
        },

        error: function(error) {
            console.log(error);
        }
    });
});
$(function() {
    setTimeout(function(){$(".loading_background, .loading_label, .wrapper").show()},100);
    $.ajax({        
        url: '/dash',
        type: 'POST',
        
        success: function(response) {  
            // Define Data
            var data = [{
                x: response.x,
                y: response.y,
                z: response.z,
                mode: "markers",
                type: "scatter3d",
                marker: {
                    color: response.c,
                    size: 1
                }
            }];

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
            
            Plotly.newPlot("point_cloud", data, layout, {displayModeBar: true}).then(function() { 
                $(".loading_background, .loading_label, .wrapper").hide();
            });
                
            // get point -> move to defined point !!
            var myPlot = document.getElementById('point_cloud');
            myPlot.on('plotly_click', function(data){
                alert(data.points[0].x + " = x")
                //console.log(data.points[0].x, data.points[0].y, data.points[0].z);
            });
        },

        error: function(error) {
            console.log(error);
        }
    });
});
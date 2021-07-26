$(function() {
    $('#depth_cam').click(function(){
        currentvalue = document.getElementById('depth_cam').value;
        
        if(currentvalue == "Off_depth"){
            console.log(currentvalue);
            $.ajax({
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "depth_cam"},
                success: function(response) {
                    $('.stream').attr("src", response.url);
                    document.getElementById("depth_cam").value="On_depth";  
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

        if(currentvalue == "On_depth"){
            console.log(currentvalue);
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {    
                    document.getElementById("depth_cam").value="Off_depth";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    })


    $('#color_cam').click(function(){
        currentvalue = document.getElementById('color_cam').value;
        
        if(currentvalue == "Off_color"){
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "color_cam"},
                success: function(response) {    
                    $('.stream').attr("src", response.url);
                    document.getElementById("color_cam").value="On_color";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

        if(currentvalue == "On_color"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {
                    document.getElementById("color_cam").value="Off_color";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });


    $('#infra_cam').click(function(){
        currentvalue = document.getElementById('infra_cam').value;
        
        if(currentvalue == "Off_infra"){
            $.ajax({
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "infra_cam"},
                success: function(response) {
                    $('.stream').attr("src", response.url);
                    document.getElementById("infra_cam").value="On_infra";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        } 

        if(currentvalue == "On_infra"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {    
                    document.getElementById("infra_cam").value="Off_infra";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

})
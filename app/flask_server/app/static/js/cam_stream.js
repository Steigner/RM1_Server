import {insert_error_cookie, allert} from './modules/cookies.js';

function anim(){
    let animation = anime({
        targets: '.image',
        borderRadius: '35%',
        duration: 800,
        easing: 'linear',
        direction: 'alternate',
        loop: true
    });
    return animation
}

function disable(){
    $("#infra_cam").prop('disabled', true);
    $("#color_cam").prop('disabled', true);
    $("#depth_cam").prop('disabled', true);
}

function undisable(){
    $("#infra_cam").prop('disabled', false);
    $("#color_cam").prop('disabled', false);
    $("#depth_cam").prop('disabled', false);
}

$(function() {
    $('#depth_cam').click(function(){
        var currentvalue = document.getElementById('depth_cam').value;

        if(currentvalue == "Off_depth"){
            disable();

            //start animation
            let animation = anim();

            $.ajax({
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "depth_cam"},
                success: function(response) {
                    // exception handling from front end
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        // stop animation get image
                        animation.restart();
                        animation.pause();
                        $('.stream').attr("src", response.url);
                        document.getElementById("depth_cam").value="On_depth";  
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

        if(currentvalue == "On_depth"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        document.getElementById("depth_cam").value="Off_depth";
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };
    })


    $('#color_cam').click(function(){
        var currentvalue = document.getElementById('color_cam').value;
        
        if(currentvalue == "Off_color"){
            disable();

            let animation = anim();
            
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "color_cam"},
                success: function(response) {
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        animation.restart();
                        animation.pause();
                        $('.stream').attr("src", response.url);
                        document.getElementById("color_cam").value="On_color";
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };

        if(currentvalue == "On_color"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        document.getElementById("color_cam").value="Off_color";
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };
    });


    $('#infra_cam').click(function(){
        var currentvalue = document.getElementById('infra_cam').value;
        
        if(currentvalue == "Off_infra"){
            disable();

            let animation = anim();

            $.ajax({
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "infra_cam"},
                success: function(response) {
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        animation.restart();
                        animation.pause();
                        $('.stream').attr("src", response.url);
                        document.getElementById("infra_cam").value="On_infra";
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };

        if(currentvalue == "On_infra"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/show_cam_stream',
                type: 'POST',
                data: {value: "stop_cam"},
                success: function(response) {    
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }
                    else{
                        document.getElementById("infra_cam").value="Off_infra";
                        undisable();
                    };
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };
    });

    // AJAX
    // Note:
    //  If click on back button stop streaming -> garbage collector.
    $(".back_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/show_cam_stream',
            type: 'POST',
            data: {value: "stop_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/con_pan";
        }, 300);
    });
})


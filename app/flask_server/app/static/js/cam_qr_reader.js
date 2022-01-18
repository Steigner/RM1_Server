import {Size} from './modules/size.js';
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

$(function() {
    var [_, _, width_devisor, _] = Size();

    $('#QR_detection').click(function(){
        var currentvalue = $("#QR_detection").val();
        let animation = anim();

        if(currentvalue == "Off_QR"){
            $(".image").css( "visibility", "visible" );
            
            $(".nav_button").animate({ 
                marginRight: (730)/width_devisor+'px'},
            );
            
            $.ajax({
                url: '/patient_menu',
                type: 'POST',
                data: {value: "QR_detection"},
                success: function(response) {
                    if(response == 'Camera is not pluged-in!'){
                        insert_error_cookie(response);
                        window.location.href="/home";
                    }

                    else{
                        animation.restart();
                        animation.pause();
                        $('.stream').attr("src", response.url);
                        document.getElementById("QR_detection").value="On_QR";  
                        $("#QR_detection").val("On_QR");
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

        if(currentvalue == "On_QR"){
            $(".image").css( "visibility", "hidden" );
            $('.stream').off();
            $('.stream').removeAttr("src");
            $(".nav_button").animate({ 
                marginLeft: (730/width_devisor)+'px'},
            );
            $.ajax({        
                url: '/patient_menu',
                type: 'POST',
                data: {value: "stop_qr_cam"},
                error: function(error) {
                    console.log(error);
                }
            });

            $.ajax({        
                url: '/store_data_qr',
                type: 'POST',
                data: {value: "store_qr_cam"},
                success: function(response) {    
                    document.getElementById("QR_detection").value="Off_QR";
                    $("#QR_detection").val("Off_QR");
                    window.location.href = "patient_data_qr";
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
        if($("#QR_detection").val() == "On_QR"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/patient_menu',
                type: 'POST',
                data: {value: "stop_qr_cam"},
                error: function(error) {
                    console.log(error);
                }
            });
            setTimeout(function(){
                window.location.href="/patient_menu";
            }, 300);
        };
    });

    $("#patient_find").click(function(){
        if($("#QR_detection").val() == "On_QR"){
            $('.stream').off();
            $('.stream').removeAttr("src");
            $.ajax({        
                url: '/patient_menu',
                type: 'POST',
                data: {value: "stop_qr_cam"},
                error: function(error) {
                    console.log(error);
                }
            });
            setTimeout(function(){
                window.location.href="/patient_find";
            }, 300);
        };
    });
})
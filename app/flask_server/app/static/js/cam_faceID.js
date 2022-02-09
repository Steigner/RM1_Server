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
    $("#face_det.next_button").prop('disabled', true);
    $(".back_button").prop('disabled', true);
}

function undisable(){
    $("#face_det.next_button").prop('disabled', false);
    $(".back_button").prop('disabled', false);
}


$(function() {
    disable();
    let animation = anim();
    // AJAX
    // Note:
    //  If click on back button stop streaming -> garbage collector.
    $(".back_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/faceID',
            type: 'POST',
            data: {value: "stop_reco_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/con_pan";
        }, 300);
    });

    // AJAX
    // Note:
    //  If click on next button stop streaming -> garbage collector.
    $("#face_det.next_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/faceID',
            type: 'POST',
            data: {value: "stop_reco_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/face_position";
        }, 3000);
    });
    

    // AJAX
    // Note:
    //  Start streaming video on response url.
    $.ajax({        
        url: '/faceID',
        type: 'POST',
        data: {value: "recognition"},
        success: function(response) {     
            if(response == 'Camera is not pluged-in!'){
                insert_error_cookie(response);
                window.location.href="/home";
            }
            else if(response == 'Patient is not init!'){
                insert_error_cookie(response);
                window.location.href="/patient_menu";
            }
            else{
                animation.restart();
                animation.pause();
                $('.stream').attr("src", response.url);
                undisable()
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
})
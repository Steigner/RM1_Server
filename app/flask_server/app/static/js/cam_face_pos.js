$(function() {    
    // AJAX
    // Note:
    //  If click on back button stop streaming -> garbage collector.
    $(".back_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/face_position',
            type: 'POST',
            data: {value: "stop_det_cam"},
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
    $("#face_val.next_button").click(function(){
        $('.stream').off();
        $('.stream').removeAttr("src");
        $.ajax({        
            url: '/face_position',
            type: 'POST',
            data: {value: "stop_det_cam"},
            error: function(error) {
                console.log(error);
            }
        });
        setTimeout(function(){
            window.location.href="/face_validation";
        }, 3000);
    });

    // AJAX
    // Note:
    //  Start streaming video on response url.
    $.ajax({        
        url: '/face_position',
        type: 'POST',
        data: {value: "position"},
        success: function(response) {     
            $('.stream').attr("src", response.url);
        },
        error: function(error) {
            console.log(error);
        }
    });
})
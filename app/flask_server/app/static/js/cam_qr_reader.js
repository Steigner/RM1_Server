import {Size} from './modules/size.js';

$(function() {
    var [_, _, width_devisor, _] = Size();

    $('#QR_detection').click(function(){

        // jquery -> here 
        //var currentvalue = document.getElementById('QR_detection').value;

        var currentvalue = $("#QR_detection").val();

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
                    $('.stream').attr("src", response.url);
                    //document.getElementById("QR_detection").value="On_QR";  
                    $("#QR_detection").val("On_QR");
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
                url: '/patient_data_qr',
                type: 'POST',
                data: {value: "stop_qr_cam"},
                success: function(response) {    
                    //document.getElementById("QR_detection").value="Off_QR";
                    $("#QR_detection").val("Off_QR");
                    window.location.href = "patient_data_qr";
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });
})
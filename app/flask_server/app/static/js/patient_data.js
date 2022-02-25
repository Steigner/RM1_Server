import {delete_warning_cookie, delete_error_cookie, insert_warning_cookie} from './modules/cookies.js';

$(function(){
    $("#face_id").prop('disabled', true);
    
    $('#select').click(function(){
        delete_warning_cookie("Patient");
        delete_error_cookie("Patient is not init!")
        insert_warning_cookie("Patient " + $("#name.data").text() + " " + $("#surname.data").text() + " was initialized!");
        $("#face_id").prop('disabled', false);
    });

    $("#gen_pdf").click(function() {
		$(".loading_background, .loading_label, .wrapper").show();
        alert("Wait for downloading!");
        setTimeout(function(){
			$(".loading_background, .loading_label, .wrapper").hide();
            window.location.href="/download";
        }, 3000);
    });

});
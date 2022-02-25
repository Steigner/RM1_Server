$(function() {
    $("#stream_cam").click(function(){
        window.location.href="/show_cam_stream"
    });

    $("#face_id").click(function() {
        $(".loading_background, .loading_label, .wrapper").show();
        window.location.href="/faceID";
    });
});
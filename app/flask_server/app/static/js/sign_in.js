/**
 * In this part we get width/height of screen
 * This will be used for compute distance of animations.
 * Devisor is so far designe for defined resolutions of some screens.
*/

var init = [];
Cookies.set('warnings', JSON.stringify(init));
Cookies.set('errors', JSON.stringify(init));

var width = window.screen.width;
var height = window.screen.height;

if (height == 960 && width == 1280){
	var height_devisor = 1;
	var width_devisor = 1;
}
if(height == 1080 && width == 1920){
	var height_devisor = 960 / 1080;
	var width_devisor = 1280 / 1920;
}

var dist = 200/height_devisor;
var plus_dist = '+=' + dist + "px"
var minus_dist = '-=' + dist + "px"

/**
 * Prepare all elements, for interaction
 * in animations, dragable functions, and so on.  
*/

// counter for clicks on keyboard_logo
var counter = 0;

$('.simple-keyboard').hide();

// need to be first defined elemet, which will be draggable
$('.simple-keyboard').draggable({});

// this prevented move with virtual keybouard out from screen resolution
$('.simple-keyboard').draggable("option", "scroll", false);

// disable, becouse after holding *.dragable_place* area, we enable it again. 
$('.simple-keyboard').draggable("disable")

// call anime svgs_logo from vk_ann_anim.js
Anime();

// after click on keyboard_logo, we use jquery simple animation function to move defined 
// elemetns up if is counter == 1, if not so second click on keyboard_logo, we use inverted function
$(document.body).on('click', '.keyboard', function () {  
  
  	counter = counter + 1;
  
  	if (counter == 1){
		$(".password").animate({ 
			marginTop : minus_dist,
		});
		
		$(".email").animate({ 
			marginTop : minus_dist,
		});
		
		$(".name_place").animate({ 
			marginTop : minus_dist,
		});
		
		$(".logo").animate({ 
			marginTop : minus_dist,
		});
		
		$(".sign_button").animate({ 
			marginTop : minus_dist,
		});
		
		// show hide virtual keyboard with animation rool up
		$(".simple-keyboard").hide().show("slide", { direction: "down" });
	}

	else{
		$(".password").animate({ 
		marginTop: plus_dist,
		});
		
		$(".email").animate({ 
		marginTop: plus_dist,
		});
		
		$(".name_place").animate({ 
		marginTop: plus_dist,
		});
		
		$(".logo").animate({ 
		marginTop: plus_dist,
		});
		
		$(".sign_button").animate({ 
		marginTop: plus_dist,
		});

		// hide showed virtual keyboard with animation rool down
		$(".simple-keyboard").hide("slide", { direction: "down" });
		
		counter = 0;
		
		Anime();
	}
});

// if we have hold left mouse button we enable dragable virtual_keyboard, 
// purpose of this function is enable only, if we hold mouse in defined aream, if not
// we just disable it, this prevent from dragable virtual keyboard from any button on vk.
$(function() {
    $('.dragable_place').on('mousedown touchstart', function(e) {
        $( ".simple-keyboard" ).draggable( "enable" );
    })
}).bind('mouseup mouseleave touchend', function() {
    $('.simple-keyboard').draggable("disable")
})
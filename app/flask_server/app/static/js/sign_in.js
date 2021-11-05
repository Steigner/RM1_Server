/**
 * In this part we get width/height of screen
 * This will be used for compute distance of animations.
 * Devisor is so far designe for defined resolutions of some screens.
*/

// hide scrollbar
document.body.style.overflow = 'hidden';

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
var plus_dist = '+=' + dist + "px";
var minus_dist = '-=' + dist + "px";

var dp_width = $('.dragable_place').width() / 2;
var dp_height = 20 / height_devisor;

/**
 * Prepare all elements, for interaction
 * in animations, dragable functions, and so on.  
*/

// counter for clicks on keyboard_logo
var counter = 0;

// find the element that you want to drag.
var box = document.getElementById('sign_in');

/* listen to the touchMove event,
every time it fires, grab the location
of touch and assign it to box */
box.addEventListener('touchmove', function(e) {
	// grab the location of touch
	var touchLocation = e.targetTouches[0];
	
	// assign box new coordinates based on the touch.
	box.style.left = (touchLocation.pageX - dp_width) + 'px';
	box.style.top = (touchLocation.pageY - dp_height) + 'px';

	e.preventDefault();
})

/* record the position of the touch
when released using touchend event.
This will be the drop position. */
box.addEventListener('touchend', function(e) {
	// current box position.
	var x = parseInt(box.style.left);
	var y = parseInt(box.style.top);
})

$('.simple-keyboard').hide();

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
				
		$(".submit_button").animate({ 
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
		
		$(".submit_button").animate({ 
		marginTop: plus_dist,
		});

		// hide showed virtual keyboard with animation rool down
		$(".simple-keyboard").hide("slide", { direction: "down" });
		
		counter = 0;
		
		Anime();
	}
});
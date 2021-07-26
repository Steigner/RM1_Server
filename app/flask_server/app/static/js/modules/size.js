export function Size() {
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

	return [width, height, width_devisor, height_devisor]
}
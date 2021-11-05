// script -> size devisor
import {Size} from './modules/size.js';

// script -> cookies manage
import {delete_warning_cookie, insert_error_cookie, insert_warning_cookie, allert} from './modules/cookies.js';

// animation of batery level
function anim(level,width_devisor){
    $(".battery_level").animate({width: ((31/width_devisor)*level)+'px'});
}

// main function
$(function battery(){
    var [e1, e2, width_devisor, e3] = Size()
    
    // get info if broswer support battery
    let isBatterySupported = 'getBattery' in navigator;

    // if not support insert warning
    if(!isBatterySupported){
        $( "#battery" ).text('warning');
        $(".not_supported_logo").css("visibility", "visible" );
        
        insert_warning_cookie("Battery is not supported!!");
        insert_error_cookie("Test cookie");
        allert();
    }

    // if yes, solve battery level
    else{

        // for case if change status
        delete_warning_cookie("Battery is not supported!!");
        allert();

        // get if battery is charging or if is running on battery
        let batteryIsCharging = false;
        navigator.getBattery().then(function(battery) {
            batteryIsCharging = battery.charging;

            // 1. init state
            if (batteryIsCharging == true){
                $(".battery_charging").css("visibility", "visible");
            }

            else{
                $(".battery").css("visibility", "visible");
                $(".battery_level").css("visibility", "visible");
                anim(battery.level, width_devisor);
            }

            $( "#battery" ).text(battery.level*100 + "%");

            // 2. wait if is change status charging / not charging state
            battery.addEventListener('chargingchange', function() {
                batteryIsCharging = battery.charging;
                
                //logo for charging
                if (batteryIsCharging == true){
                    $(".battery").css("visibility", "hidden");
                    $(".battery_charging").css("visibility", "visible");
                    anim(battery.level, width_devisor);
                }
                
                //simple battery level
                else{
                    anim(battery.level, width_devisor);
                    $(".battery").css("visibility", "visible");
                    $(".battery_charging").css("visibility", "hidden");
                }
            });

            // 3. changing battery level state
            battery.addEventListener('levelchange', function() {
                $( "#battery" ).text(battery.level*100 + "%");
                anim(battery.level, width_devisor);
            });
        });
    }
});
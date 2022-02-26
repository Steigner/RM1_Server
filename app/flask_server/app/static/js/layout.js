import { Size } from './modules/size.js';
import { num_errors, num_warnings } from './modules/cookies.js';

var [width, height, width_devisor, _] = Size();

$('#bottom_panel').css({ width: 60 / width_devisor + 'px' });

// this should go be called first
$('.cover').hide();

$('.info_num').hide();
$('.info_button').hide();
$('#sign_out').hide();
$('#home').hide();

$('.info_button').prop('disabled', true);
$('#sign_out').prop('disabled', true);
$('#home').prop('disabled', true);

$('.cover').css({
    width: width,
    height: height,
});

var counter = 0;
var count_w = 0;
var count_e = 0;

$(document.body).on('click', '#roll_button', function () {
    counter = counter + 1;

    if (counter == 1) {
        num_warnings();
        num_errors();

        $('.cover').fadeIn('slow');
        $('#bottom_panel').animate(
            { width: 1150 / width_devisor + 'px' },

            function () {
                $('.info_button').prop('disabled', false);
                $('#sign_out').prop('disabled', false);
                $('#home').prop('disabled', false);

                $('.info_num').fadeIn('slow');
                $('.info_button').fadeIn('slow');
                $('#sign_out').fadeIn('slow');
                $('#home').fadeIn('slow');
            }
        );

        anime({
            targets: '#roll_button',
            rotateZ: '360deg',
            duration: 3000,
        });
    } else {
        $('.placeholder').children('.toast').remove();
        count_e = 0;
        count_w = 0;

        $('.cover').fadeOut();

        $('#bottom_panel').animate({ width: 60 / width_devisor + 'px' }, 1500);

        counter = 0;

        $('.info_num').fadeOut();
        $('.info_button').fadeOut();
        $('#sign_out').fadeOut();
        $('#home').fadeOut();
        $('.info_button').prop('disabled', true);
        $('#sign_out').prop('disabled', true);
        $('#home').prop('disabled', true);

        anime({
            targets: '#roll_button',
            rotateZ: '-360deg',
            duration: 3000,
        });
    }
});

// WARNINGS
$('#warning.info_button').click(function () {
    count_w += 1;

    if (count_w == 1) {
        var cookies = JSON.parse(Cookies.get('warnings'));

        for (var cookie of cookies) {
            $('.placeholder').append('<div class="toast">' + cookie + '</div>');
        }
    } else {
        // delete all divs
        count_w = 0;
        count_e = 0;
        $('.placeholder').children('.toast').remove();
    }
});

// ERRORS
$('#error.info_button').click(function () {
    count_e += 1;

    if (count_e == 1) {
        var cookies = JSON.parse(Cookies.get('errors'));
        for (var cookie of cookies) {
            $('.placeholder').append(
                '<div class="toast" style="background: #722f37">' +
                    cookie +
                    '</div>'
            );
        }
    } else {
        // delete all divs
        count_e = 0;
        count_w = 0;
        $('.placeholder').children('.toast').remove();
    }
});

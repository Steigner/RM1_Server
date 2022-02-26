// find div .wrapper
const wrapperEl = document.querySelector('.wrapper');
// set number of elements which will be add
const numberOfEls = 70;
// set up duration of one cycle of infinity loop
const duration = 6000;
// delay which is set up for each element
const delay = duration / numberOfEls;

let tl = anime.timeline({
    duration: delay,
    complete: function () {
        tl.restart();
    },
});

// create alll 60 element in circle
function createEl(i) {
    // find first element and add another in circle
    let el = document.createElement('div');
    const rotate = (360 / numberOfEls) * i;

    // compute by resolution this ...
    const translateY = -50;

    el.classList.add('el');
    // define color
    el.style.backgroundColor = 'hsl(193, 26%, 62%)';

    el.style.transform =
        'rotate(' + rotate + 'deg) translateY(' + translateY + '%)';
    tl.add({
        begin: function () {
            anime({
                targets: el,
                backgroundColor: ['hsl(193, 26%, 62%)', 'hsl(193, 58%, 31%)'],
                rotate: [rotate + 'deg', rotate + 10 + 'deg'],
                translateY: [translateY + '%', translateY + 10 + '%'],
                scale: [1, 1.25],
                easing: 'easeInOutSine',
                direction: 'alternate',
                duration: duration * 0.1,
            });
        },
    });
    wrapperEl.appendChild(el);
}

for (let i = 0; i < numberOfEls; i++) createEl(i);

$('.loading_background, .loading_label, .wrapper').show();

$(window).on('load', function () {
    setTimeout(function () {
        $('.loading_background, .loading_label, .wrapper').hide();
    }, 100);
    //$(".loading_background, .loading_label, .wrapper").hide();
});

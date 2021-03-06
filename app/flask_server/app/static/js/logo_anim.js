function Anime() {
    anime({
        targets: '.logo #Layer_1 .cls-4',
        fill: ['rgba(0,0,0,0)', '#21697c'],
        easing: 'easeInOutSine',
        duration: 4000,
    });

    anime({
        targets: '.logo #Layer_1 .cls-3',
        fill: ['rgba(0,0,0,0)', '#85acb7'],
        easing: 'easeInOutSine',
        duration: 4000,
    });

    anime({
        targets: '.password_logo,.email_logo, .cls-5, .cls-6 ',
        strokeDashoffset: [anime.setDashoffset, 0],
        easing: 'easeInOutSine',
        duration: 3500,
    });
}

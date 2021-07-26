export function allert(){
    anime({
        targets: '.cls-2l',
        fill: '#21697c',
        easing: 'easeInOutQuad',
        direction: 'alternate',
        loop: 2
    });
};

export function num_warnings(){
    var warnings = JSON.parse(Cookies.get('warnings'));
    $("#num_warnings.text").text(warnings.length);
};

export function num_errors(){
    var errors = JSON.parse(Cookies.get('errors'));
    $("#num_errors.text").text(errors.length);
};
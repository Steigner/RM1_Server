let Keyboard = window.SimpleKeyboard.default;

let keyboard = new Keyboard({
    onChange: (input) => onChange(input),
    onKeyPress: (button) => onKeyPress(button),
    disableButtonHold: true,
    theme: 'hg-theme-default NumKey',
    layout: {
        default: ['7 8 9', '4 5 6', '1 2 3', '0 . {bksp}'],
    },
});

document.querySelector('.ip_input').addEventListener('input', (event) => {
    keyboard.setInput(event.target.value);
});

function onChange(input) {
    document.querySelector('.ip_input').value = input;
}

function onKeyPress(button) {}

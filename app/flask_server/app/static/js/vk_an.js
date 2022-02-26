let Keyboard = window.SimpleKeyboard.default;
let selectedInput;

let keyboard = new Keyboard({
    onChange: (input) => onChange(input),
    onKeyPress: (button) => onKeyPress(button),
    disableButtonHold: true,
    theme: 'hg-theme-default AlfanumKey',
});

document.querySelectorAll('.input').forEach((input) => {
    input.addEventListener('focus', onInputFocus);
    input.addEventListener('input', onInputChange);
});

function onInputFocus(event) {
    selectedInput = `#${event.target.id}`;

    keyboard.setOptions({
        inputName: event.target.id,
    });
}

function onInputChange(event) {
    keyboard.setInput(event.target.value, event.target.id);
}

function onChange(input) {
    //console.log("Input changed", input);
    document.querySelector(selectedInput || '.input').value = input;
}

function onKeyPress(button) {
    //console.log("Button pressed", button);
    if (button === '{lock}' || button === '{shift}') handleShiftButton();
    if (button === '{enter}') {
        $('.submit_button').click();
    }
}

function handleShiftButton() {
    let currentLayout = keyboard.options.layoutName;
    let shiftToggle = currentLayout === 'default' ? 'shift' : 'default';

    keyboard.setOptions({
        layoutName: shiftToggle,
    });
}

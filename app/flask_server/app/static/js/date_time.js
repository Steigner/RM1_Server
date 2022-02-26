function updateTime() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDate();
    var hours = date.getHours();
    var minutes = date.getMinutes();

    // Fastest way to get two digit
    if (day < 10) {
        var day = '0' + day;
    }

    if (month < 10) {
        var month = '0' + month;
    }

    if (hours < 10) {
        var hours = '0' + hours;
    }

    if (minutes < 10) {
        var minutes = '0' + minutes;
    }

    var date = day + '.' + month + '.' + year;
    var time = hours + ':' + minutes;

    $('#date').text(date);
    $('#time').text(time);
}
setInterval(updateTime, 100);

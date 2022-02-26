// script -> size devisor
import { Size } from './modules/size.js';

import { insert_error_cookie, allert } from './modules/cookies.js';

class RobotInspection {
    constructor() {
        this.add_info_input();
    }

    // public method:
    //   input: none
    //   return none
    // Note: change default setting of doughnout charts from chart.js, and add
    // inside this chart text value.
    add_info_input() {
        Chart.pluginService.register({
            beforeDraw: function (chart) {
                if (chart.config.options.elements.center) {
                    // Get ctx from string
                    var ctx = chart.chart.ctx;

                    // Get options from the center object in options
                    var centerConfig = chart.config.options.elements.center;
                    var fontStyle = centerConfig.fontStyle || 'Arial';
                    var txt = centerConfig.text;
                    var color = centerConfig.color || '#000';
                    var maxFontSize = centerConfig.maxFontSize || 75;
                    var sidePadding = centerConfig.sidePadding || 20;
                    var sidePaddingCalculated =
                        (sidePadding / 100) * (chart.innerRadius * 2);
                    // Start with a base font of 30px
                    ctx.font = '30px ' + fontStyle;

                    // Get the width of the string and also the width of the element minus 10 to give it 5px side padding
                    var stringWidth = ctx.measureText(txt).width;
                    var elementWidth =
                        chart.innerRadius * 2 - sidePaddingCalculated;

                    // Find out how much the font can grow in width.
                    var widthRatio = elementWidth / stringWidth;
                    var newFontSize = Math.floor(30 * widthRatio);
                    var elementHeight = chart.innerRadius * 2;

                    // Pick a new font size so it will not be larger than the height of label.
                    var fontSizeToUse = Math.min(
                        newFontSize,
                        elementHeight,
                        maxFontSize
                    );
                    var minFontSize = centerConfig.minFontSize;
                    var lineHeight = centerConfig.lineHeight || 25;
                    var wrapText = false;

                    if (minFontSize === undefined) {
                        minFontSize = 20;
                    }

                    if (minFontSize && fontSizeToUse < minFontSize) {
                        fontSizeToUse = minFontSize;
                        wrapText = true;
                    }

                    // Set font settings to draw it correctly.
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    var centerX =
                        (chart.chartArea.left + chart.chartArea.right) / 2;
                    var centerY =
                        (chart.chartArea.top + chart.chartArea.bottom) / 2;
                    ctx.font = fontSizeToUse + 'px ' + fontStyle;
                    ctx.fillStyle = color;

                    if (!wrapText) {
                        ctx.fillText(txt, centerX, centerY);
                        return;
                    }

                    var words = txt.split(' ');
                    var line = '';
                    var lines = [];

                    // Break words up into multiple lines if necessary
                    for (var n = 0; n < words.length; n++) {
                        var testLine = line + words[n] + ' ';
                        var metrics = ctx.measureText(testLine);
                        var testWidth = metrics.width;
                        if (testWidth > elementWidth && n > 0) {
                            lines.push(line);
                            line = words[n] + ' ';
                        } else {
                            line = testLine;
                        }
                    }

                    // Move the center up depending on line height and number of lines
                    centerY -= (lines.length / 2) * lineHeight;

                    for (var n = 0; n < lines.length; n++) {
                        ctx.fillText(lines[n], centerX, centerY);
                        centerY += lineHeight;
                    }

                    //Draw text in center
                    ctx.fillText(line, centerX, centerY);
                }
            },
        });
    }

    // public method:
    //   input: none
    //   return none
    // Note: get all charts, and AJAX to server for data from robot via
    // python socket communication!
    connect_server() {
        // get every init charts in html
        var [charts] = this.charts_get();

        $.ajax({
            url: '/robot_inspection',
            type: 'POST',
            data: { value: 'data_feed' },
            success: function (response) {
                if (response == 'Robot is not connected!') {
                    insert_error_cookie(response);
                    allert();
                } else {
                    if (!!window.EventSource) {
                        var source = new EventSource(response);
                        // onmessage parse data from response url
                        source.onmessage = function (e) {
                            var string = e.data;
                            var data = JSON.parse('[' + string + ']')[0];

                            // 0-5 currenct charts -> update it
                            function update_chart_curr(data, chart) {
                                chart.data.datasets[0].data[0] = data;
                                chart.data.datasets[0].data[1] = 5 - data;
                                // set up info center input - current
                                chart.options.elements.center.text =
                                    data.toFixed(2) + ' A';
                                chart.update();
                            }

                            // 6-11 temperature charts -> update it
                            function update_chart_temp(data, chart) {
                                chart.data.datasets[0].data[0] = data;
                                chart.data.datasets[0].data[1] = 60 - data;
                                // set up info center input - temperature
                                chart.options.elements.center.text =
                                    data.toFixed(1) + ' °C';
                                chart.update();
                            }

                            for (var i in data) {
                                // 0 -> 5
                                if (i <= 5) {
                                    update_chart_curr(data[i], charts[i]);
                                }
                                // 6 -> 11
                                else {
                                    update_chart_temp(data[i], charts[i]);
                                }
                            }
                        };
                    }

                    // IMPORTANT !! before leave, stop streaming data!
                    $(window).on('beforeunload', function () {
                        source.close();
                    });
                }
            },
            error: function (error) {
                console.log(error);
            },
        });
    }

    // public method:
    //   input: none
    //   return none
    // Note: set up new added feature -> level inside chart
    charts_settings() {
        var option = {
            hover: { mode: null },
            tooltips: { enabled: false },
            animation: { duration: 1000 },
            responsive: true,

            rotation: -Math.PI / 2,

            maintainAspectRatio: false,
            cutoutPercentage: 82.5,
            elements: {
                center: {
                    text: '',
                    color: 'rgba(33, 105, 124, 1)', // Default is #000000
                    fontStyle: 'Verdana, sans-serif', // Default is Arial
                    sidePadding: 35, // Default is 20 (as a percentage)
                    minFontSize: 10, // Default is 20 (in px), set to false and text will not wrap.
                    lineHeight: 20, // Default is 25 (in px), used for when text wraps
                },
            },
        };

        var dataset = {
            backgroundColor: [
                'rgba(33, 105, 124, 1)', // darkgreen
                'rgba(242, 242, 242, 1)', // grey
            ],
            borderWidth: 0,
            data: [0, 5],
        };

        return [option, dataset];
    }

    // public method:
    //   input: charts
    //   return none
    // Note: defualt set up charts
    chart_set(id_chart) {
        var [option, dataset] = this.charts_settings();

        var chart = new Chart($(id_chart)[0].getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [dataset],
            },
            options: option,
        });

        return chart;
    }

    // public method:
    //   input: none
    //   return none
    // Note: init all charts of temperature and current from html
    charts_get() {
        var elements = [
            '#curr_base',
            '#curr_shoulder',
            '#curr_elbow',
            '#curr_wrist_1',
            '#curr_wrist_2',
            '#curr_wrist_3',
            '#temp_base',
            '#temp_shoulder',
            '#temp_elbow',
            '#temp_wrist_1',
            '#temp_wrist_2',
            '#temp_wrist_3',
        ];

        var charts = [];

        // set up all charts
        for (var element of elements) {
            var chart = this.chart_set(element);
            charts.push(chart);
        }

        return [charts];
    }
}

/* MAIN */
$(function () {
    let robot = new RobotInspection();

    robot.connect_server();

    var [e1, e2, width_devisor, e4] = Size();
    var counter = 0;

    $('.robot').hide();
    $('#label').hide();

    // interactivity with vector graphics of UR3 from html!
    $('.show').click(function () {
        counter = counter + 1;
        if (counter == 1) {
            $('.show').hide();

            $('.sidebar').animate({ width: 400 / width_devisor + 'px' });
            $('.robot').fadeIn('slow');
            $('#label').fadeIn('slow');

            $('#wrist_3_joint').click(function () {
                $('#wrist_3_joint').css({ opacity: '1' });
                $(
                    '#wrist_2_joint, #wrist_1_joint, #elbow_joint, #shoulder_joint, #base_joint'
                ).css({ opacity: '0.4' });
                $('#label').text('Engine 6');
            });

            $('#wrist_2_joint').click(function () {
                $('#wrist_2_joint').css({ opacity: '1' });
                $(
                    '#wrist_3_joint, #wrist_1_joint, #elbow_joint, #shoulder_joint, #base_joint'
                ).css({ opacity: '0.4' });
                $('#label').text('Engine 5');
            });

            $('#wrist_1_joint').click(function () {
                $('#wrist_1_joint').css({ opacity: '1' });
                $(
                    '#wrist_3_joint, #wrist_2_joint, #elbow_joint, #shoulder_joint, #base_joint'
                ).css({ opacity: '0.4' });
                $('#label').text('Engine 4');
            });

            $('#elbow_joint').click(function () {
                $(
                    '#wrist_3_joint, #wrist_2_joint, #wrist_1_joint, #shoulder_joint, #base_joint'
                ).css({ opacity: '0.4' });
                $('#elbow_joint').css({ opacity: '1' });
                $('#label').text('Engine 3');
            });

            $('#shoulder_joint').click(function () {
                $('#shoulder_joint').css({ opacity: '1' });
                $(
                    '#wrist_3_joint, #wrist_2_joint, #wrist_1_joint, #elbow_joint, #base_joint'
                ).css({ opacity: '0.4' });
                $('#label').text('Engine 2');
            });

            $('#base_joint').click(function () {
                $(
                    '#wrist_3_joint, #wrist_2_joint, #wrist_1_joint, #elbow_joint, #shoulder_joint'
                ).css({ opacity: '0.4' });
                $('#base_joint').css({ opacity: '1' });
                $('#label').text('Engine 1');
            });
            $('.show').fadeIn('slow');
        } else {
            $('.show').fadeOut();
            $('.sidebar').animate({ width: 52 / width_devisor + 'px' });
            $('.robot').fadeOut();
            $('#label').fadeOut();
            counter = 0;
            $('.show').fadeIn('slow');
        }
    });
});

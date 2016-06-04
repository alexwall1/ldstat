jQuery(document).ready(function($) {
    $.getJSON("static/json/employer_summary.json", function(employer_summary_data) {
        $("#employer-summary-chart").highcharts({
            chart: {
                type: 'bubble',
                plotBorderWidth: 1,
                zoomType: 'xy'
            },

            legend: {
                enabled: false
            },

            title: {
                text: 'De största annonsörerna'
            },
            subtitle: {
                text: 'Källa: Platsbanken',
                x: -20
            },
            xAxis: {
                gridLineWidth: 1,
                title: {
                    text: 'Antal yrkesområden'
                },
                labels: {
                    format: '{value} st'
                },
                plotLines: [{
                    color: 'black',
                    dashStyle: 'dot',
                    width: 2,
                    value: 65,
                    label: {
                        rotation: 0,
                        y: 15,
                        style: {
                            fontStyle: 'italic'
                        }
                    },
                    zIndex: 3
                }]
            },

            yAxis: {
                startOnTick: false,
                endOnTick: false,
                title: {
                    text: 'Antal län'
                },
                labels: {
                    format: '{value} st'
                },
                maxPadding: 0.2,
                plotLines: [{
                    color: 'black',
                    dashStyle: 'dot',
                    width: 2,
                    value: 50,
                    label: {
                        align: 'right',
                        style: {
                            fontStyle: 'italic'
                        },
                        x: -10
                    },
                    zIndex: 3
                }]
            },

            tooltip: {
                useHTML: true,
                headerFormat: '<table>',
                pointFormat: '<tr><th colspan="2"><h3>{point.employer_name}</h3></th></tr>' +
                    '<tr><th>Antal yrkesområden:</th><td>{point.x} st</td></tr>' +
                    '<tr><th>Antal län:</th><td>{point.y} st</td></tr>' +
                    '<tr><th>Antal platsannonser:</th><td>{point.z} st</td></tr>',
                footerFormat: '</table>',
                followPointer: true
            },

            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true,
                        format: '{point.employer_name}'
                    }
                }
            },

            series: [{
                data: employer_summary_data
            }]
        });
    });
});
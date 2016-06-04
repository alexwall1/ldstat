jQuery(document).ready(function($) {
    $.getJSON("static/json/professional_area_time_series.json", function(time_series_data) {
        $("#professional-area-chart").highcharts({
        title: {
            text: 'Antal annonser per vecka och yrkesomr�de',
            x: -20 //center
        },
        subtitle: {
            text: 'K�lla: Platsbanken',
            x: -20
        },
        xAxis: {
            categories: time_series_data['x_labels']
        },
        yAxis: {
            title: {
                text: 'Annonser per yrkesomr�de'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: ' annonser'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: time_series_data['result']
        });
    });
});
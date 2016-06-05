jQuery(document).ready(function($) {
    var chart = null;
    var $backButton = $("#back");
    var prefix = '';

    var options = {
        chart: {
            renderTo: 'chart'
        },
        title: {
            text: "Antal annonser per vecka och yrkesomr\u00E5de",
            x: -20 //center
        },
        subtitle: {
            text: 'K\u00E4lla: Platsbanken',
            x: -20
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Antal annonser'
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
        plotOptions: {
            series: {
                events: {
//                    legendItemClick: function(e) {
//                        console.log('clicked legend for series ' + this.index);
//                        var series = this.chart.series;
//                        for (var i = 0; i < series.length; i++) {
//                            if (series[i].index != this.index) {
//                                console.log('series[' + i + '].visible: ' + series[i].visible);
//                                series[i].visible ? series[i].hide() : series[i].show();
//                            }
//                        }
//                    }
                },
                cursor: 'pointer',
                point: {
                    events: {
                        click: function(e) {
                            getProfessionalArea(this.series.options.id, this.series.options.name);
                        }
                    }
                }
            }
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            borderWidth: 0
        }
    };

    var getProfessionalGroup = function(professional_area_id,
    professional_area_name,
    county_id,
    county_name) {
        // third level
        $.getJSON(prefix + "/professional_group_weekly?county_id="
        + county_id
        + "&professional_area_id="
        + professional_area_id, function(obj) {
            var series = [];
            for (var series_id in obj) {
                series.push(obj[series_id]);
            }
            options.title.text = 'Antal annonser per vecka f\u00F6r ' + professional_area_name + ' i ' + county_name;
            options.series = series;

//            options.plotOptions.series.point.events.click = function(e) {
//                window.location.href = '/ldstat/posts/' + this.series.options.id + '/' + county_id;
//            };

//            $backButton.off();
//            $backButton.click(function() {
//                alert('just clicked third');
//            });
//            $backButton.show();

            chart = new Highcharts.Chart(options)
        });
    };

    var getProfessionalArea = function(professional_area_id, professional_area_name, previousOptions) {
        // second level
        $.getJSON(prefix + "/professional_area_weekly?professional_area_id=" + professional_area_id, function(obj) {
            var series = [];

            for (var series_id in obj) {
                series.push(obj[series_id]);
            }

            options.title.text = 'Antal annonser per vecka f\u00F6r ' + professional_area_name;
            options.series = series;
            options.plotOptions.series.point.events.click = function(e) {
                getProfessionalGroup(professional_area_id,
                professional_area_name,
                this.series.options.id,
                this.series.options.name);
            };

/*            $backButton.click(function(previousOptions) {
                chart = new Highcharts.Chart(previousOptions);
            });

            $backButton.show();*/

            chart = new Highcharts.Chart(options)
        });
    };

    $.getJSON(prefix + "/professional_area_weekly", function(obj) {
        // first level
        // $backButton.hide();

        var series = [];
        for (var series_id in obj) {
            series.push(obj[series_id]);
        }

        options.series = series;
        chart = new Highcharts.Chart(options);
    });
});
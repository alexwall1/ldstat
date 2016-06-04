jQuery(document).ready(function($) {
    var nest = function(keys, data, rollupFunction) {
        var _nest = d3.nest();
        keys.forEach(function(key) {
            _nest.key(function(d) { return d[key]; });
        });
        if (rollupFunction) {
            _nest.rollup(rollupFunction);
        }
        return _nest.entries(data);
    };

    var allSums = function(v) {
        return {
            num_posts_w1: d3.sum(v, function(d) { return d.num_posts_w1; }),
            num_jobs_w1: d3.sum(v, function(d) { return d.num_jobs_w1; }),
            num_posts_w0: d3.sum(v, function(d) { return d.num_posts_w0; }),
            num_jobs_w0: d3.sum(v, function(d) { return d.num_jobs_w0; }),
            distinct_num_posts: d3.sum(v, function(d) { return d.distinct_num_posts; })
        };
    }

    $.getJSON("static/json/profession_per_municipality_weekly.json", function(data) {
        postsByProfessionalArea = nest(['professional_area_name'], data, allSums);
        var $outputTable = $('#output');
        $outputTable.empty();


        $outputTable.append('<tr><th>Yrkesområde</th><th>Antal annonser</th><th>Antal jobb</th><th>Unika annonser</th></tr>');
        for (var i = 0; i < postsByProfessionalArea.length; i++) {

//            changeNumPosts = postsByProfessionalArea[i].values.num_posts_w0 > 0 ?
//                (postsByProfessionalArea[i].values.num_posts_w1 - postsByProfessionalArea[i].values.num_posts_w0) / postsByProfessionalArea[i].values.num_posts_w0 :
//                0;
//            changeNumJobs = postsByProfessionalArea[i].values.num_jobs_w0 > 0 ?
//                (postsByProfessionalArea[i].values.num_jobs_w1 - postsByProfessionalArea[i].values.num_jobs_w0) / postsByProfessionalArea[i].values.num_jobs_w0 :
//                0;

            $("#output").append('<tr>'+
                '<td>' + postsByProfessionalArea[i].key + '</td>' +
                '<td>' + postsByProfessionalArea[i].values.num_posts_w1 + '</td>' +
                // '<td>' + changeNumPosts + '</td>' +
                '<td>' + postsByProfessionalArea[i].values.num_jobs_w1 + '</td>' +
                // '<td>' + changeNumJobs + '</td>' +
                '<td>' + postsByProfessionalArea[i].values.distinct_num_posts + '</td>' +
            '</tr>');
        }
    });
});

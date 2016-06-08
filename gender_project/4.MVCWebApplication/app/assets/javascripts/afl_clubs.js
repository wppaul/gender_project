y = [13.2419624288296,13.5078926732808,14.3977361835601,11.8884456718148,9.43711431591149,8.52340527087382,11.7418431011558,8.72796699737479,8.53363335719887]
function showChart(){
    // Create the chart
    $('#afl_clubs').highcharts({
        chart: {
            type: 'pie'
        },
        title: {
            text: ' Melbourne based AFL clubs Gender Profile'
        },
        subtitle: {
            text: 'Click the slices to view each club'
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.y:.1f}%'
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },
        series: [{
            name: 'Clubs',
            colorByPoint: true,
            data: [{
                name: 'Carlton',
                y: y[0],
                drilldown: 'Carlton'
            }, {
                name: 'Collinwood',
                y: y[1],
                drilldown: 'Collinwood'
            }, {
                name: 'Stkilda',
                y: y[8] ,
                drilldown: 'Stkilda'
            }, {
                name: 'Hawthorn',
                y: y[3],
                drilldown: 'Hawthorn'
            }, {
                name: 'Melbourne',
                y: y[4],
                drilldown: 'Melbourne'
            }, {
                name: 'Richmond',
                y: y[6],
                drilldown: 'Richmond'
            },{
                name: 'Essendon',
                y: y[2],
                drilldown: 'Essendon'
            },{
                name: 'NorthMelbourne',
                y: y[5],
                drilldown: 'NorthMelbourne'
            },{
                name: 'WesternBulldog',
                y: y[8],
                drilldown: 'WesternBulldog'
            }]
        }],
        drilldown: {
            series: [{
                name: 'Carlton',
                id: 'Carlton',
                data: [
                    ['male', 68.3831101956746],
                    ['female', 31.6168898043254],
                ]
            }, {
                name: 'Collinwood',
                id: 'Collinwood',
                data: [
                    ['male', 66.65825340737],
                    ['female', 33.34174659263],
                ]
            }, {
                name: 'Essendon',
                id: 'Essendon',
                data: [
                    ['male', 68.3874023206251],
                    ['female', 31.6125976793749],
                ]
            }, {
                name: 'Hawthorn',
                id: 'Hawthorn',
                data: [
                    ['male', 69.3432750215085],
                    ['female', 30.6567249784915],
                ]
            }, {
                name: 'Melbourne',
                id: 'Melbourne',
                data: [
                    ['male', 70.6647398843931],
                    ['female', 29.3352601156069],
                ]
            }, {
                name: 'NorthMelbourne',
                id: 'NorthMelbourne',
                data: [
                    ['male', 71.72],
                    ['female', 28.28],
                ]
            }, {
                name: 'Richmond',
                id: 'Richmond',
                data: [
                    ['male', 69.3670150987224],
                    ['female', 30.6329849012776],
                ]
            }, {
                name: 'Stkilda',
                id: 'Stkilda',
                data: [
                    ['male', 70.1171875],
                    ['female', 29.8828125],
                ]
            }, {
                name: 'WesternBulldog',
                id: 'WesternBulldog',
                data: [
                    ['male', 70.1558130243707],
                    ['female', 29.8441869756292],
                ]
            }]
        }
    });

}




function nametest(){
    femaleName();
    maleName();
}
function femaleName() {
    $('#female-container').highcharts({
        chart: {
            type: 'bar'
        },
        colors: [
          '#ffa64d',
          '#33ccff',
        ],
        title: {
            text: 'Top Female Names of the Twitter users in Melbourne'
        },
        subtitle: {
            text: 'Source: couchdb'
        },
        xAxis: {
            categories: ['Sarah', 'Michelle', 'Kate', 'Emily', 'Lisa','Emma','Laura','Jessica','Nicole','Rebecca','Amy','Amanda'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of Times Used',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 30,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Female',
            data: [165, 113, 105, 90, 85,85,80,78,71,71,69,59]
        }],
    });
}

function maleName() {
    $('#male-container').highcharts({
        chart: {
            type: 'bar'
        },
        colors: [
          '#33ccff',
        ],
        title: {
            text: 'Top Male Names of the Twitter users in Melbourne'
        },
        subtitle: {
            text: 'Source: couchdb'
        },
        xAxis: {
            categories: ['Michael', 'David','Andrew','Paul', 'John','Mark','Matthew','James','Peter','Adam','Daniel','Tim'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of Times Used',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -20,
            y: 30,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Male',
            data: [322, 315, 279, 255, 238,232,228,218,193,190,187,169]
        }],
    });
}

function comparemale(){
        $('#commale').highcharts({

        chart: {
            polar: true,
            type: 'line'
        },

        title: {
            text: 'Predict Name vs Real Name 1970-1979',
            x: -80
        },

        pane: {
            size: '80%'
        },

        xAxis: {
            categories: ['Michael', 'David','Andrew','Paul', 'John','Mark','Matthew','James','Peter','Adam','Daniel','Tim'],
            tickmarkPlacement: 'on',
            lineWidth: 0
        },

        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },

        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },

        series: [{
            name: 'Predict Male Names',
            data: [322, 315, 279, 255, 238,232,228,218,193,190,187,169],
            pointPlacement: 'on'
        }, {
            name: 'Real Name 1970-1979 Top Male Names',
            data: [328,346,312,293,154,257,295,132,179,180,223,127],
            pointPlacement: 'on'
        }]
    });
}


function comparefemale(){
    $('#comfemale').highcharts({

        chart: {
            polar: true,
            type: 'line'
        },

        title: {
            text: 'Predict Name vs Real Name 1980-1989',
            x: -80
        },

        pane: {
            size: '80%'
        },

        xAxis: {
            categories: ['Sarah', 'Michelle', 'Kate', 'Emily', 'Lisa','Emma','Laura','Jessica','Nicole','Rebecca','Amy','Amanda'],
            tickmarkPlacement: 'on',
            lineWidth: 0
        },

        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },

        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },

        series: [{
            name: 'Predict Female Names',
            data: [165, 113, 105, 90, 85,85,80,78,71,71,69,59],
            pointPlacement: 'on'
        }, {
            name: 'Real Name 1980-1989 Top Female Names',
            data: [168,66,69,56,61,83,66,157,80,131,64,70],
            pointPlacement: 'on'
        }]
    });
}
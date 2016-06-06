//Place all the behaviors and hooks related to the matching controller here.
//All this logic will automatically be available in application.js

var chart_name = ["club","shopping"];
var name_list =[[{name: 'male', y: 20292}, {name: 'female', y: 9039}],[{name: 'male', y: 1026}, {name: 'female', y: 1834}]];
// change club!!!!!!!!!!!!!!!
// function downloadData(){
//     $.ajax({
//         url: 'http://115.146.89.191:5984/all_clubs/_design/analysis/_view/find_clubs?group_level=1',
//         type: 'get',
//         dataType: 'jsonp',
//         success: function(data){
//             for(var i = 0; i < data.rows.length; i++){
//                 temp = {name: data.rows[i].key, y: data.rows[i].value}
//                 name_list.push(temp);
//             }
//             drawpie();
//             name_list = [];
//         }
//     });
// }
function thetest(){
    for(var i = 0; i < chart_name.length; i++){
        drawpie(chart_name[i],name_list[i])
    }
}

// function processingData(char_name,data){
//     var name_list = [];
//     for(var i = 0; i < data.rows.length; i++){
//         temp = {name: data.rows[i].key, y: data.rows[i].value}
//         name_list.push(temp);
//     };
//     drawpie(char_name,name_list)
// }

function drawpie(chart_name, data_list) {
    $('#'+chart_name+'-container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            backgroundColor:'rgba(255, 255, 255, 0.6)'
        },
        colors: [
          '#33ccff',
          '#ff8080', 

        ],
        title: {
            text: chart_name
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'percentage',
            colorByPoint: true,
            data: data_list
        }]
    });
}




function drawshop(){
        $('#shop').highcharts({
        chart: {
            type: 'column'
        },
                colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: 'Shopping Average Sentiment'
        },
        xAxis: {
            categories: [
                'Shopping Average Sentiment',
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.3f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'female',
            data: [0.1789567599758605]

        },{
            name: 'male',
            data: [0.16163955363578036]

        }
        ]
    });

}

function drawclub(){
        $('#club').highcharts({
        chart: {
            type: 'column'
        },
                colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: 'Club Average Sentiment'
        },
        xAxis: {
            categories: [
                'Club Average Sentiment',
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.3f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'female',
            data: [0.16223866985547]

        },{
            name: 'male',
            data: [0.136625793165129]

        }
        ]
    });

}
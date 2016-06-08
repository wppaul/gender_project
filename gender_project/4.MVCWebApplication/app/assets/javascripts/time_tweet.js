name_list_female =[];
name_list_male =[];
male_hour = [];
female_hour=[];
male_user_hour = [];
female_user_hour = []
male_user_day = [];
female_user_day = []
female_hour_user = []
male_hour_user = []

function showbar(){
    downloadfemaleData();
    downloadmaleData();
    downloadhourfemaleData();
    downloadhourmaleData();
    downloadhourfemaleuser();
    downloadhourmaleuser();
}

function downloadfemaleData(){
    $.ajax({
        url: 'http://115.146.89.193:5984/female_tweet_dayofweek_new/_design/helper/_view/week',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (name_list_female.length <7){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                name_list_female.push(data.rows[i].value['count']);
                }
            }

            linechart();
        }
    });
}

function downloadmaleData(){
    $.ajax({
        url: 'http://115.146.89.193:5984/male_tweet_dayofweek_new/_design/helper/_view/week',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (name_list_male.length <7){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                name_list_male.push(data.rows[i].value['count']);
                }


            }
            linechart();
        }
    });
}

function downloadhourfemaleData(){
    $.ajax({
        url: 'http://115.146.89.193:5984/female_tweet_hour_new/_design/helper/_view/female_hour',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (female_hour.length <24){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                    female_hour.push(data.rows[i].value['count']);
                }
            }

            dayLine();
        }
    });
}

function downloadhourmaleData(){
    $.ajax({
        url: 'http://115.146.89.193:5984/male_tweet_hour_new/_design/helper/_view/male_hour',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (male_hour.length <24){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                    male_hour.push(data.rows[i].value['count']);
                }
            }

            dayLine();
        }
    });
}

function downloadhourfemaleuser(){
    $.ajax({
        url: 'http://115.146.89.193:5984/female_user_hour_new/_design/helper/_view/fuser',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (female_hour_user.length <24){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                    female_hour_user.push(data.rows[i].value['count']);
                }
            }

            userdayLine();
        }
    });
}

function downloadhourmaleuser(){
    $.ajax({
        url: 'http://115.146.89.193:5984/male_user_hour_new/_design/helper/_view/muser',
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            if (male_hour_user.length <24){
                for(var i = 0; i < data.rows.length; i++){
                // temp = {name: data.rows[i].key, y: data.rows[i].value}
                    male_hour_user.push(data.rows[i].value['count']);
                }
            }

            userdayLine();
        }
    });
}

function linechart(){
    $('#week-container').highcharts({
        chart: {
            type: 'column',
        },
        colors: [
                  '#ff8080', 
                  '#33ccff',
                ],
        title: {
            text: 'Tweets Volume Calculation for a Week'
        },
        subtitle: {
            text: 'Source: couchdb'
        },
        xAxis: {
            categories: [
                'SUN',
                'MON',
                'TUE',
                'WED',
                'THUR',
                'FRI',
                'SAT'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'NO.of Tweets sent'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
            }

        },
        series: [{
            name: 'Female',
            data: name_list_female
            // [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0]

        }, {
            name: 'Male',
            data: name_list_male
            // [42.4, 33.2, 34.5, 39.7, 52.6, 75.5, 57.4]

        }]
    });
}

// Data retrieved from http://vikjavev.no/ver/index.php?spenn=2d&sluttid=16.06.2015.
function dayLine() {
    $('#day-container').highcharts({
        chart: {
            type: 'spline'
        },
        colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: 'Tweets Volume Calculation for a Day'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'time',
            tickInterval: 1,
            labels: {
                overflow: 'justify'
            }
        },
        yAxis: {
            title: {
                text: 'No. of Tweets'
            },
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            alternateGridColor: null,
            plotBands: [{ // Light air
                from: 0,
                to: 50,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {   
                    text: '',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Light breeze
                from: 50,
                to: 100,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { 
                from: 100,
                to: 150,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Moderate breeze
                from: 150,
                to: 200,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Fresh breeze
                from: 8,
                to: 11,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Strong breeze
                from: 11,
                to: 14,
                color: 'rgba(0, 0, 0, 0)',
            }, { // High wind
                from: 14,
                to: 15,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }]
        },
        tooltip: {
            valueSuffix: ' '
        },
        plotOptions: {
            spline: {
                lineWidth: 4,
                states: {
                    hover: {
                        lineWidth: 5
                    }
                },
                marker: {
                    enabled: false
                },
                // pointInterval: 1, // one hour
                // pointStart: Time.UTC(0, 0, 0)
            }
        },
        series: [{
            name: 'Female',
            data: [female_hour[0],female_hour[1],female_hour[12],female_hour[17],female_hour[18],female_hour[19],female_hour[20],female_hour[21],female_hour[22],female_hour[23],female_hour[2],female_hour[3],female_hour[4],female_hour[5],female_hour[6],female_hour[7],female_hour[8],female_hour[9],female_hour[10],female_hour[11],female_hour[13],female_hour[14],female_hour[15],female_hour[16]]
            // [0.2, 0.8, 0.8, 0.8, 1, 1.3, 1.5, 2.9, 1.9, 2.6, 1.6, 3, 4, 3.6, 4.5, 4.2, 4.5, 4.5, 4, 3.1, 2.7, 4, 2.7, 2.3, 2.3, 4.1, 7.7, 7.1, 5.6, 6.1, 5.8, 8.6, 7.2, 9, 10.9, 11.5, 11.6, 11.1, 12, 12.3, 10.7, 9.4, 9.8, 9.6, 9.8, 9.5, 8.5, 7.4, 7.6]

        }, {
            name: 'Male',
            data: [male_hour[0],male_hour[1],male_hour[12],male_hour[17],male_hour[18],male_hour[19],male_hour[20],male_hour[21],male_hour[22],male_hour[23],male_hour[2],male_hour[3],male_hour[4],male_hour[5],male_hour[6],male_hour[7],male_hour[8],male_hour[9],male_hour[10],male_hour[11],male_hour[13],male_hour[14],male_hour[15],male_hour[16]]
            // [female_hour[0],female_hour[1],female_hour[12],female_hour[17],female_hour[18],female_hour[19],female_hour[20],female_hour[21],female_hour[22],female_hour[23],female_hour[2],female_hour[3],female_hour[4],female_hour[5],female_hour[6],female_hour[7],female_hour[8],female_hour[9],female_hour[10],female_hour[11],female_hour[13],female_hour[14],female_hour[15],female_hour[16]]
            // [0, 0, 0.6, 0.9, 0.8, 0.2, 0, 0, 0, 0.1, 0.6, 0.7, 0.8, 0.6, 0.2, 0, 0.1, 0.3, 0.3, 0, 0.1, 0, 0, 0, 0.2, 0.1, 0, 0.3, 0, 0.1, 0.2, 0.1, 0.3, 0.3, 0, 3.1, 3.1, 2.5, 1.5, 1.9, 2.1, 1, 2.3, 1.9, 1.2, 0.7, 1.3, 0.4, 0.3]
        }],
        navigation: {
            menuItemStyle: {
                fontSize: '10px'
            }
        }
    });
}

function userdayLine() {
    $('#user-container').highcharts({
        chart: {
            type: 'spline'
        },
        colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: 'Tweets users Calculation for a Day'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'time',
            tickInterval: 1,
            labels: {
                overflow: 'justify'
            }
        },
        yAxis: {
            title: {
                text: 'No. of Tweets'
            },
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            alternateGridColor: null,
            plotBands: [{ // Light air
                from: 0,
                to: 50,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {   
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Light breeze
                from: 50,
                to: 100,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { 
                from: 100,
                to: 150,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Moderate breeze
                from: 150,
                to: 200,
                color: 'rgba(0, 0, 0, 0)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Fresh breeze
                from: 8,
                to: 11,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }, { // Strong breeze
                from: 11,
                to: 14,
                color: 'rgba(0, 0, 0, 0)',
            }, { // High wind
                from: 14,
                to: 15,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: ' ',
                    style: {
                        color: '#606060'
                    }
                }
            }]
        },
        tooltip: {
            valueSuffix: ' '
        },
        plotOptions: {
            spline: {
                lineWidth: 4,
                states: {
                    hover: {
                        lineWidth: 5
                    }
                },
                marker: {
                    enabled: false
                },
                // pointInterval: 1, // one hour
                // pointStart: Time.UTC(0, 0, 0)
            }
        },
        series: [{
            name: 'Female',
            data: [female_hour_user[0],female_hour_user[1],female_hour_user[12],female_hour_user[17],female_hour_user[18],female_hour_user[19],female_hour_user[20],female_hour_user[21],female_hour_user[22],female_hour_user[23],female_hour_user[2],female_hour_user[3],female_hour_user[4],female_hour_user[5],female_hour_user[6],female_hour_user[7],female_hour_user[8],female_hour_user[9],female_hour_user[10],female_hour_user[11],female_hour_user[13],female_hour_user[14],female_hour_user[15],female_hour_user[16]]
            // [0.2, 0.8, 0.8, 0.8, 1, 1.3, 1.5, 2.9, 1.9, 2.6, 1.6, 3, 4, 3.6, 4.5, 4.2, 4.5, 4.5, 4, 3.1, 2.7, 4, 2.7, 2.3, 2.3, 4.1, 7.7, 7.1, 5.6, 6.1, 5.8, 8.6, 7.2, 9, 10.9, 11.5, 11.6, 11.1, 12, 12.3, 10.female_hour_user7, 9.4, 9.8, 9.6, 9.8, 9.5, 8.5, 7.4, 7.6]

        }, {
            name: 'Male',
            data: [male_hour_user[0],male_hour_user[1],male_hour_user[12],male_hour_user[17],male_hour_user[18],male_hour_user[19],male_hour_user[20],male_hour_user[21],male_hour_user[22],male_hour_user[23],male_hour_user[2],male_hour_user[3],male_hour_user[4],male_hour_user[5],male_hour_user[6],male_hour_user[7],male_hour_user[8],male_hour_user[9],male_hour_user[10],male_hour_user[11],male_hour_user[13],male_hour_user[14],male_hour_user[15],male_hour_user[16]]
            // [female_hour[0],female_hour[1],female_hour[12],female_hour[17],female_hour[18],female_hour[19],female_hour[20],female_hour[21],female_hour[22],female_hour[23],female_hour[2],female_hour[3],female_hour[4],female_hour[5],female_hour[6],female_hour[7],female_hour[8],female_hour[9],female_hour[10],female_hour[11],female_hour[13],female_hour[14],female_hour[15],female_hour[16]]
            // [0, 0, 0.6, 0.9, 0.8, 0.2, 0, 0, 0, 0.1, 0.6, 0.7, 0.8, 0.6, 0.2, 0, 0.1, 0.3, 0.3, 0, 0.1, 0, 0, 0, 0.2, 0.1, 0, 0.3, 0, 0.1, 0.2, 0.1, 0.3, 0.3, 0, 3.1, 3.1, 2.5, 1.5, 1.9, 2.1, 1, 2.3, 1.9, 1.2, 0.7, 1.3, 0.4, 0.3]
        }],
        navigation: {
            menuItemStyle: {
                fontSize: '10px'
            }
        }
    });
}

function combine(){
        $('#combine').highcharts({
        title: {
            text: 'Twitter users of the Week and Average Sentiment'
        },
        xAxis: {
            categories: ['SUN', 'MON','TUE','WED','THUR','FRI','SAT'],
        },
                colors: [
                  '#ff8080', 
                  '#33ccff',
                ],
        
        labels: {
            items: [{
                html: '',
                style: {
                    left: '50px',
                    top: '18px',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                }
            }]
        },
        series: [ 
        {
            type: 'column',
            name: 'Female',
            data:[7227,
7874,
7072,
7342,
7671,
7334,
7475]
        },{
            type: 'column',
            name: 'Male',
            data: [11317,12177,11190,11270,11916,11859,11854]
        }, {
            type: 'spline',
            name: 'Female Average',
            data: [14635.3141426009,
13867.4236028971,
14216.3554400116,
13665.3168849873,
14244.3839992521,
14188.3726929375,
14451.2932450278
            ],
            marker: {
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[2],
                fillColor: 'white'
            }
        },{
            type: 'spline',
            name: 'Male Average',
            data: [12187.6005160606,
11985.5265089621,
11922.708494305,
12523.7120238201,
12389.2514546247,
12359.4558072739,
11679.0135325363],
            marker: {
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[1],
                fillColor: 'white'
            }
        }]
    });
}
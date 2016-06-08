// This script is showing the club vs shopping
var chart_name = ["club","shopping"];

// request club data from database
function renderClubData(){
    $.ajax({
        url: database + club_gender,
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            club_male = [];
            club_female = [];
            club_male_sentiment = [];
            club_female_sentiment = [];
            for(var i = 0; i < data.rows.length; i++){     
                club_male.push(data.rows[i].value[0]); 
                club_female.push(data.rows[i].value[1]);
                club_male_sentiment.push(data.rows[i].value[2]);
                club_female_sentiment.push(data.rows[i].value[3]);     
            }
            processClubData(club_male,club_female,club_male_sentiment,club_female_sentiment);
        }
    });
}

function processClubData(club_male,club_female,club_male_sentiment,club_female_sentiment){
    var totalmale = 0;
    var totalmale_sentiment = 0;
    for (i=0; i<club_male.length; i++){
        totalmale += club_male[i];
        totalmale_sentiment += club_male_sentiment[i];
    }
    var totalfemale = 0;
    var totalfemale_sentiment = 0
    for (i=0; i<club_female.length; i++){
        totalfemale += club_female[i];
        totalfemale_sentiment += club_female_sentiment[i];
    }
    var sentiment_data = []
    sentiment_data.push(totalfemale_sentiment/9);
    sentiment_data.push(totalmale_sentiment/9);
    club_list = [{name: 'male', y: totalmale}, {name: 'female', y: totalfemale}];
    drawpie(chart_name[0],club_list);
    drawbar('club','Club Average Sentiment',sentiment_data);
}

// request shopping data from database
function renderShoppingData(){
    $.ajax({
        url: database + shopping_gender,
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            shop_female = data.rows[0].value[0];
            shop_male = data.rows[1].value[0];
            female_sentiment = data.rows[0].value[1];
            male_sentiment = data.rows[1].value[1];      
            processShoppingData(shop_female,shop_male,female_sentiment,male_sentiment);
        }
    });
}

function processShoppingData(shop_female,shop_male,female_sentiment,male_sentiment){
    shop_list = [{name: 'male', y: shop_male}, {name: 'female', y: shop_female}];
    data = [female_sentiment,male_sentiment];
    drawpie(chart_name[1],shop_list);
    drawbar('shop','Shopping Average Sentiment',data);
}

//draw pie chart
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

//draw bar chart
function drawbar(name,title,data){
        $('#'+ name).highcharts({
        chart: {
            type: 'column'
        },
                colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: title
        },
        xAxis: {
            categories: [
                title
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
            data: [data[0]]

        },{
            name: 'male',
            data: [data[1]]

        }
        ]
    });
}
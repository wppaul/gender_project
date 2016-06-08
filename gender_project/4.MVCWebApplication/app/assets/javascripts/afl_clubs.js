// request data and render view
function renderData(){
    $.ajax({
        url: database + club_gender,
        type: 'get',
        dataType: 'jsonp',
        success: function(data){
            club_name = [];
            club_male = [];
            club_female = [];
            for(var i = 0; i < data.rows.length; i++){   
                club_name.push(data.rows[i].key);    
                club_male.push(data.rows[i].value[0]); 
                club_female.push(data.rows[i].value[1]);     
            }
            processData(club_name,club_male,club_female);
        }
    });
}

// process data and draw chart
function processData(club_name,club_male,club_female){
    var totalmale = 0;
    for (i=0; i<club_male.length; i++){
        totalmale += club_male[i];
    }

    var totalfemale = 0;
    for (i=0; i<club_female.length; i++){
        totalfemale += club_female[i];
    }
    club_total = totalmale + totalfemale;

    var male_percentage = [];
    var female_percentage = [];
    var club_percentage = [];
    for (i=0; i<club_male.length; i++){
        temp_male = club_male[i]/(club_male[i]+club_female[i])*100;
        temp_female = club_female[i]/(club_male[i]+club_female[i])*100;
        temp_club = (club_male[i]+club_female[i])/club_total*100;
        male_percentage.push(temp_male);
        female_percentage.push(temp_female);
        club_percentage.push(temp_club);
    }
    showChart(club_name,male_percentage,female_percentage,club_percentage);
}

function showChart(club_name,male_percentage,female_percentage,club_percentage){
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
                name: club_name[0],
                y: club_percentage[0],
                drilldown: club_name[0]
            }, {
                name: club_name[1],
                y: club_percentage[1],
                drilldown: club_name[1]
            }, {
                name: club_name[7],
                y: club_percentage[7],
                drilldown: club_name[7]
            }, {
                name: club_name[3],
                y: club_percentage[3],
                drilldown: club_name[3]
            }, {
                name: club_name[4],
                y: club_percentage[4],
                drilldown: club_name[4]
            }, {
                name: club_name[6],
                y: club_percentage[6],
                drilldown: club_name[6]
            },{
                name: club_name[2],
                y: club_percentage[2],
                drilldown: club_name[2]
            },{
                name: club_name[5],
                y: club_percentage[5],
                drilldown: club_name[5]
            },{
                name: club_name[8],
                y: club_percentage[8],
                drilldown: club_name[8]
            }]
        }],
        drilldown: {
            series: [{
                name: club_name[0],
                id: club_name[0],
                data: [
                    ['male',male_percentage[0]],
                    ['female',female_percentage[0]],
                ]
            }, {
                name: club_name[1],
                id: club_name[1],
                data: [
                    ['male',male_percentage[1]],
                    ['female',female_percentage[1]],
                ]
            }, {
                name: club_name[2],
                id: club_name[2],
                data: [
                    ['male',male_percentage[2]],
                    ['female',female_percentage[2]],
                ]
            }, {
                name: club_name[3],
                id: club_name[3],
                data: [
                    ['male',male_percentage[3]],
                    ['female',female_percentage[3]],
                ]
            }, {
                name: club_name[4],
                id: club_name[4],
                data: [
                    ['male',male_percentage[4]],
                    ['female',female_percentage[4]],
                ]
            }, {
                name: club_name[5],
                id: club_name[5],
                data: [
                    ['male',male_percentage[5]],
                    ['female',female_percentage[5]],
                ]
            }, {
                name: club_name[6],
                id: club_name[6],
                data: [
                    ['male',male_percentage[6]],
                    ['female',female_percentage[6]],
                ]
            }, {
                name: club_name[7],
                id: club_name[7],
                data: [
                    ['male',male_percentage[7]],
                    ['female',female_percentage[7]],
                ]
            }, {
                name: club_name[8],
                id: club_name[8],
                data: [
                    ['male',male_percentage[8]],
                    ['female',female_percentage[8]],
                ]
            }]
        }
    });
}
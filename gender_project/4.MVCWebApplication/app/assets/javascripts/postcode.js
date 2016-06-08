var polyMap 
var mapData={"polygon":[],"data":[]}
var threshold={"people": [1000,3000,5000,10000,30000,50000],
               "male": [100,500,2000,5000,10000,20000],
               "female": [100,500,2000,5000,10000,20000]
}
var poly_continue_flag= true;
var current_feature = "overview"
var color_threshold=['#e6e6ff','#ccccff','#9999ff','#8080ff','#6666ff','#3333ff','#1a1aff']

function initPolyMap() {
  polyMap = new google.maps.Map(document.getElementById('map'), {
    zoom: 9,
    center: melbourne_center_coordinates,
    mapTypeId: google.maps.MapTypeId.HYBRID
  });
  poly_continue_flag= true;
  getPostcodesCall(setPolyToMap);
}

function coordsParser(Coords){
  var listOfCoords = []
  for (var i = 0; i < Coords.length; i++){
    singleSet = Coords[i];
    listOfCoords.push({lat: singleSet[0], lng:singleSet[1]});
  }
  return listOfCoords;
}
function getContent(properties){
  return '<table class="table"><tbody> <tr> <td>Postcode</td> <td>'+properties.postcode
  +'<tr> <td>Suburb</td> <td>'+properties.suburb
  +'<tr> <td>People</td> <td>'+properties.people
  +'</td> </tr><tr> <td> Male Sentiment</td> <td>'+properties.male_sentiment_over_3.toFixed(6)
  +'</td> </tr><tr> <td> Female Sentiment</td> <td>'+properties.female_sentiment_over_3.toFixed(6)
  +'</td> </tr><tr> <td> Average Children</td> <td>'+properties.averagechildren
  +'</td> </tr><tr> <td> Unemployment Rate</td> <td>'+properties.unemploymentrate
  +'</td> </tr> </tbody> </table>';
}

function getFeatureContent(){
  if(current_feature=="overview"){
    return "";
  }
  var current_threshold=threshold[current_feature];
  var content='<table><tbody>';
  for (var i = 0; i < current_threshold.length; i++){
    content+= '<tr> <td style="width:15px; background:'+color_threshold[i]+' "></td> <td> <'+threshold[current_feature][i]+'</td> </tr>'
  }
  return content+='<tr> <td style="background:'+color_threshold[6]+' "></td> <td> >'+threshold[current_feature][5]+'</td> </tr> <tr> <td style="width:15px; background: #000033;"></td> <td> notcoverded </td> </tr></tbody> </table>';
}

function updatePanelData(data){
  var content=getContent(data.properties);
  $("#surburd-name").text(data.properties.name);
  $("#panel-data").html(content);
}
function getCorrespondingColor(data){
  switch(current_feature){
    case "overview":
      return '#FFFFF0';
    case "people":
      return getRespond(data.properties.people);
    case "male":
      return getRespond(data.properties.male);
    case "female":
      return getRespond(data.properties.female);
  }
  return "#000000"
}
function getRespond(attribute){
  thresholdLst=threshold[current_feature]
  for (var i = 0; i < thresholdLst.length; i++){
    if (attribute<thresholdLst[i]){
      return color_threshold[i]
    }
  }
  return attribute > thresholdLst[5] ? color_threshold[6] : '#000000'
}
function setPolyToMap(data){
  // Construct the polygon.
  cords=coordsParser(data.geometry.coordinates);

  var polygon = new google.maps.Polygon({
    paths: cords,
    strokeColor: '#ff8c1a',
    strokeOpacity: 0.5,
    strokeWeight: 1,
    fillColor: getCorrespondingColor(data),
    fillOpacity: 0.5,
    map: polyMap
  });
  google.maps.event.addListener(polygon, "mousemove", function(event) {
    polygon.setOptions({strokeColor: "#000000"});
    polygon.setOptions({strokeWeight: 4});
    updatePanelData(data);
    show(data);
  });
  google.maps.event.addListener(polygon, "mouseout", function(event) {
    polygon.setOptions({strokeColor: "#1a8cff"});
    polygon.setOptions({strokeWeight: 1});
  });
  mapData["polygon"].push(polygon);
  mapData["data"].push(data);
}

function setFeatureData(feature){
  current_feature=feature;
  polyLst=mapData["polygon"];
  dataLst=mapData["data"];
  $("#legend-data").html(getFeatureContent());
  for (var i = 0; i < polyLst.length; i++){
    polyLst[i].setOptions({fillColor:getCorrespondingColor(dataLst[i])})
  }
}

function show(data){
        male1 = parseFloat(data.properties.male_ratio_over_1_new)
        female1 = parseFloat(data.properties.female_ratio_over_1_new)
        male2 = parseFloat(data.properties.male_ratio_over_2_new)
        female2 = parseFloat(data.properties.female_ratio_over_2_new)
        male3 = parseFloat(data.properties.male_ratio_over_3_new)
        female3 = parseFloat(data.properties.female_ratio_over_3_new)
        male = parseFloat(data.properties.malepercentage)/100
        female = parseFloat(data.properties.femalepercentage)/100


    $('#show').highcharts({
        chart: {
            type: 'column'
        },
                colors: [
          '#ff8080', 
          '#33ccff',
        ],
        title: {
            text: 'Gender Ratio Based on Tweets Count'
        },
        subtitle: {
            text: 'Source: Couchdb'
        },
        xAxis: {
            categories: [
                'Over#1',
                'Over#2',
                'Over#3',
                'Actural'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'No.of Twitter Users'
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
                    dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.y:.1f}%'
                },
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                dataLabels: {
                  enabled:true,
                  format: "{point.y:.2f}"
                }
            }
        },
        series: [{
            name: 'Female',
            data: [female1, female2,female3,female]

        }, {
            name: 'Male',
            data: [male1, male2,male3,male]

        }]
    });
}





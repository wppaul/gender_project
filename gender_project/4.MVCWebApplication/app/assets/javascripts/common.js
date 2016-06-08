var database = 'http://115.146.89.193:5984';
var club_gender = '/club_gender_count_new/_design/analysis/_view/club_gender_count'
var shopping_gender = '/shopping_gender_count_new/_design/analysis/_view/shopping_gender_count'
var melbourne_center_coordinates={lat: -37.816480, lng: 144.965914}
var hostAddr = 'http://115.146.89.191:5984';
var suburb='/absdata';
var female_id_coordinates_address = '/all_female_new/_design/analysis/_view/female_heat'
// '/essentialbaby/_design/analysis/_view/female_heat';
var male_id_coordinates_address = '/all_male_new/_design/analysis/_view/male_heat'
// '/essentialbaby/_design/analysis/_view/male_heat';

function isUndefined(data,request_data){
    return (typeof data == "undefined") ? "undefined" : data[request_data];
}

function getFixedNumber(number, fixedpoint){
    if(isNaN(number)){return number;}
    return Number((number).toFixed(fixedpoint));
}

function getPostcodesCall(rowHandler){
  $.ajax({
    url: hostAddr + suburb+'/_all_docs',
    type: 'get',
    dataType: 'jsonp',
    success: function(data) {
      suburb_data_rows=data.rows.length;
      // suburb_data_rows=300;
      for(var i = 0; i < suburb_data_rows; i++){
        var pCodeUrl = hostAddr + suburb + '/' + data.rows[i].id;
        getPcodeData(pCodeUrl,rowHandler);
      }
    }
  });
}

function getPcodeData(pCodeUrl,rowHandler){
  $.ajax({
    url: pCodeUrl,
    type: 'get',
    dataType: 'jsonp',
    success: function(data) {
      rowHandler(data);
    }
  });
}
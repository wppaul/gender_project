# encoding=utf8  
import sys 
import json
import couchdb
import requests
reload(sys)  
sys.setdefaultencoding('utf8')

couch = couchdb.Server('http://115.146.89.191:5984')
counter = 0
try:
	data_base = couch.create('melbourne_tweets')
except couchdb.http.PreconditionFailed as e:
	data_base = couch['melbourne_tweets']

countlist = []
for row in data_base.view('helper/checkpostcode'):
    countlist.append(row['key'])
    # lat_long = str(latitude) + "," + str(longitude)
    # location = geolocator.reverse(lat_long)
    # return [location.raw['address']['postcode'],location.raw['address']['suburb']]
geoGoogle = "http://maps.googleapis.com/maps/api/geocode/json?address="
s = requests.Session()

for doc_id in countlist[10000:12500]:
    data = data_base[doc_id]
    if counter >= 2500:
        break
    suburb = ""
    postal_code = ""
    if data['coordinates'] != None:
        lat = data['coordinates']["coordinates"][1]
        lon = data['coordinates']["coordinates"][0]
        reverse_geocode_result = s.post(geoGoogle+str(lat)+','+str(lon))
        result_string = reverse_geocode_result.json()
        json_result = result_string['results']
        if not json_result:
            print ("no result or api reach the limit")
            break
        for result in json_result:
            for address in result['address_components']:
                if suburb == "" or postal_code == "":
                    if address['types'] == ['locality', 'political']:
                        suburb = address['long_name']
                        print (suburb)
                    if address['types'] == ['postal_code']:
                        postal_code = address['long_name']
                        print (postal_code)
        if suburb != "" or postal_code != "":
            data['suburb'] = suburb
            data['postal_code'] = postal_code
            data['has_coor'] = 'True'
        else:
            data['suburb'] = ""
            data['postal_code'] = '0000'
            data['has_coor'] = 'False'
        counter += 1
    else:
        data['suburb'] = ""
        data['postal_code'] = '0000'
        data['has_coor'] = 'False'
    data_base.save(data)
    print ("There has %d tweets has been modified! "%counter)
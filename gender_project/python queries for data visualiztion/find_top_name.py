import re
import csv
import couchdb
import json

def to_each_name(source_db, target_db):
	map_fun = '''function(doc) {
        emit(doc.firstname,doc.sentiment_score)
	}'''
	reduce_fun = '''function(keys, values, rereduce) {
    	if (!rereduce){
        	var length = values.length
        	return [sum(values) / length, length]
    	}else{
        	var length = sum(values.map(function(v){return v[1]}))
        	var average = sum(values.map(function(v){
            	return v[0] * (v[1] / length)
            	}))
        	return [average, length]
    	}
	}'''

	count = 1
	json_result = {}
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result['firstname'] = row.key
		json_result['sentiment_score'] = row.value[0]
		json_result['count'] = row.value[1]
		target_db[str(count)] = json_result
		count += 1

def to_each_user(source_db, target_db):
	map_fun = '''function(doc) {
    	if(doc.gender == 'female'){
        	emit([doc.user.name.split(' ',1)[0].toLowerCase(), doc.user.id],doc.sentiment_score)
	    }
	}'''
	reduce_fun = '''function(keys, values, rereduce) {
    	if (!rereduce){
        	var length = values.length
        	return sum(values) / length
    	}else{
        	var length = sum(values.map(function(v){return v[1]}))
        	var average = sum(values.map(function(v){
            	return v[0] * (v[1] / length)
            	}))
        	return average
    	}
	}'''

	count = 1
	json_result = {}
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result['firstname'] = row.key[0]
		json_result['userid'] = row.key[1]
		json_result['sentiment_score'] = row.value
		target_db[str(count)] = json_result
		count += 1

couch = couchdb.Server('http://115.146.89.191:5984/')
# couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	source_database = couch.create('melbourne_tweets')
except couchdb.http.PreconditionFailed as e:
	source_database = couch['melbourne_tweets']

couch = couchdb.Server('http://115.146.89.193:5984/')
couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	target_database1 = couch.create('female_names')
except couchdb.http.PreconditionFailed as e:
	del couch['female_names']
	target_database1 = couch.create('female_names')

couch = couchdb.Server('http://115.146.89.193:5984/')
couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	target_database2 = couch.create('top_female_names')
except couchdb.http.PreconditionFailed as e:
	del couch['top_female_names']
	target_database2 = couch.create('top_female_names')


to_each_user(source_database, target_database1)
to_each_name(target_database1, target_database2)

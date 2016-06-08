import re
import csv
import couchdb
import json

def add_suburb_male_count(source_db, target_db, suffix):
	map_fun = '''function(doc) {
        emit(doc._id,[doc.count, doc.sentiment_score])
	}'''

	suburb_gender = {}
	for row in source_db.query(map_fun).rows:
		if row.key in target_db:
			document = target_db[row.key]
			document['properties']['male_over_' + suffix] = row.value[0]
			document['properties']['male_sentiment_over_' + suffix] = row.value[1]
			target_db.save(document)

def add_suburb_female_count(source_db, target_db, suffix):
	map_fun = '''function(doc) {
        emit(doc._id,[doc.count, doc.sentiment_score])
	}'''

	suburb_gender = {}
	for row in source_db.query(map_fun).rows:
		if row.key in target_db:
			document = target_db[row.key]
			document['properties']['female_over_' + suffix] = row.value[0]
			document['properties']['female_sentiment_over_' + suffix] = row.value[1]
			if 'male_over_' + suffix in document['properties']:
				document['properties']['female_ratio_over_' + suffix] = row.value[0] / float(row.value[0] + document['properties']['male_over_' + suffix])
				document['properties']['male_ratio_over_' + suffix] = 1 - document['properties']['female_ratio_over_' + suffix]
			else:
				document['properties']['female_ratio_over_' + suffix] = 1
				document['properties']['male_ratio_over_' + suffix] = 1 - document['properties']['female_ratio_over_' + suffix]
			target_db.save(document)

def connect_database(ip, dbname):
	couch = couchdb.Server(ip)
	couch.resource.credentials = ('wppaul', 'qwert12345')
	try:
		source_database = couch.create(dbname)
	except couchdb.http.PreconditionFailed as e:
		source_database = couch[dbname]
	return source_database
	
couch = couchdb.Server('http://115.146.89.191:5984/')
# couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	target_database = couch.create('absdata')
except couchdb.http.PreconditionFailed as e:
	target_database = couch['absdata']

source_database1 = connect_database('http://115.146.89.193:5984/', 'male_user_over_1_new')
source_database2 = connect_database('http://115.146.89.193:5984/', 'female_user_over_1_new')
add_suburb_male_count(source_database1, target_database, '1_new')
add_suburb_female_count(source_database2, target_database, '1_new')


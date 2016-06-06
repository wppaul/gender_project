import re
import couchdb

def tweet_dayofweek(source_db, gender):
	map_fun = '''function(doc) {
        var date = new Date(doc.created_at);
        TZO = -600;
        date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
        var day = date.getDay();
		emit(day, doc.sentiment_score);
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

	db_name = gender + '_tweet_dayofweek_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'count': row.value[1], 'sentiment_score': row.value[0]}
		target_db[str(row.key)] = json_result

def tweet_hour(source_db, gender):
	map_fun = '''function(doc) {
        var date = new Date(doc.created_at);
        TZO = -600;
        date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
        var hour = date.getHours();
        emit(hour, doc.sentiment_score);
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

	db_name = gender + '_tweet_hour_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'count': row.value[1], 'sentiment_score': row.value[0]}
		target_db[str(row.key)] = json_result

def prepare_user_dayofweek(source_db, gender):
	map_fun = '''function(doc) {
        var date = new Date(doc.created_at);
        TZO = -600;
        date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
        var day = date.getDay();
		emit([doc.user.id, day], doc.sentiment_score);
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
	db_name = 'prepare_' + gender + '_user_dayofweek_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'user_id': row.key[0], 'dayofweek': row.key[1], 'sentiment_score': row.value}
		target_db[str(count)] = json_result
		count += 1
	return target_db

def prepare_user_hour(source_db, gender):
	map_fun = '''function(doc) {
        var date = new Date(doc.created_at);
        TZO = -600;
        date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
        var hour = date.getHours();
        emit([doc.user.id, hour], doc.sentiment_score);
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
	db_name = 'prepare_' + gender + '_user_hour_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'user_id': row.key[0], 'hour': row.key[1], 'sentiment_score': row.value}
		target_db[str(count)] = json_result
		count += 1
	return target_db
    
def user_dayofweek(source_db, gender):
	map_fun = '''function(doc) {
        emit(doc.dayofweek, doc.sentiment_score);
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

	db_name = gender + '_user_dayofweek_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'count': row.value[1], 'sentiment_score': row.value[0]}
		target_db[str(row.key)] = json_result

def user_hour(source_db, gender):
	map_fun = '''function(doc) {
        emit(doc.hour, doc.sentiment_score);
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

	db_name = gender + '_user_hour_new'
	target_db = create_database(db_name)
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		json_result = {'count': row.value[1], 'sentiment_score': row.value[0]}
		target_db[str(row.key)] = json_result


def create_database(name):
	couch = couchdb.Server('http://115.146.89.193:5984/')
	couch.resource.credentials = ('wppaul', 'qwert12345')
	try:
		target_database = couch.create(name)
	except couchdb.http.PreconditionFailed as e:
		del couch[name]
		target_database = couch.create(name)
	return target_database


couch = couchdb.Server('http://115.146.89.193:5984/')
couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	source_database1 = couch.create('all_male_new')
except couchdb.http.PreconditionFailed as e:
	source_database1 = couch['all_male_new']

couch = couchdb.Server('http://115.146.89.193:5984/')
couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	source_database2 = couch.create('all_female_new')
except couchdb.http.PreconditionFailed as e:
	source_database2 = couch['all_female_new']

tweet_dayofweek(source_database1, 'male')
tweet_dayofweek(source_database2, 'female')
tweet_hour(source_database1, 'male')
tweet_hour(source_database2, 'female')
pre_db1 = prepare_user_dayofweek(source_database1, 'male')
pre_db2 = prepare_user_dayofweek(source_database2, 'female')
pre_db3 = prepare_user_hour(source_database1, 'male')
pre_db4 = prepare_user_hour(source_database2, 'female')
user_dayofweek(pre_db1, 'male')
user_dayofweek(pre_db2, 'female')
user_hour(pre_db3, 'male')
user_hour(pre_db4, 'female')

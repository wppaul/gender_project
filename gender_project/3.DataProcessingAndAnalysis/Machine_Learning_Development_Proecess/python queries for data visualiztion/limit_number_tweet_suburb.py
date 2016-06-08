import re
import couchdb

def prepare_limit_number_user(source_db, gender, number):
    map_fun = '''function(doc) {
        if(doc.postal_code && doc.user.id){
            emit([doc.user.id, doc.postal_code], doc.sentiment_score)
        }
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
    # postal_code_tweet = {}
    db_name = 'prepare_' + gender + '_user_over_' + str(number) + '_new'
    target_db = create_database(db_name)
    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        user_id = row.key[0]
        postal_code = row.key[1]
        # print row.key
        # print row.value
        if row.value[1] >= number:
            json_result = {'userid': user_id, 'postal_code': row.key[1], 'sentiment_score': row.value[0]}
            target_db[str(count)] = json_result
            # if postal_code not in postal_code_tweet:
            #     postal_code_tweet[postal_code] = row.value[1]
            # else:
            #     postal_code_tweet[postal_code] += row.value[1]
            count += 1
    return target_db

def upload_limit_number_user_amount(source_db, gender, number):
    map_fun = '''function(doc) {
        emit(doc.postal_code, doc.sentiment_score)
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
    db_name = gender + '_user_over_' + str(number) + '_new'
    target_db = create_database(db_name)
    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        json_result = {'sentiment_score': row.value[0], 'count': row.value[1]}
        target_db[row.key] = json_result
        count += 1

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


pre_db11 = prepare_limit_number_user(source_database1, 'male', 1)
pre_db12 = prepare_limit_number_user(source_database2, 'female', 1)
upload_limit_number_user_amount(pre_db11, 'male', 1)
upload_limit_number_user_amount(pre_db12, 'female', 1)

pre_db21 = prepare_limit_number_user(source_database1, 'male', 2)
pre_db22 = prepare_limit_number_user(source_database2, 'female', 2)
upload_limit_number_user_amount(pre_db21, 'male', 2)
upload_limit_number_user_amount(pre_db22, 'female', 2)

pre_db31 = prepare_limit_number_user(source_database1, 'male', 3)
pre_db32 = prepare_limit_number_user(source_database2, 'female', 3)
upload_limit_number_user_amount(pre_db31, 'male', 3)
upload_limit_number_user_amount(pre_db32, 'female', 3)


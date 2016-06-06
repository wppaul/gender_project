import re
import couchdb

def find_club_user(source_db):
    map_fun = '''function(doc) {
        var club_list = ["Melbourne", "Richmond", "Carlton", "Hawthorn", "Collingwood", "StKilda", "Essendon", "NorthMelbourne", "WesternBulldogs"];
        for(i = 0; i< club_list.length; i++){
            for(j = 0; j< doc.club.length; j++){
                 if((doc.club[i] == doc.club[j])&&(doc.gender)){
                     emit([doc.club[j],doc.user.id_str, doc.gender],doc.sentiment_score);
                 }
            }
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
    db_name = 'all_club_users_new'
    target_db = create_database(db_name)
    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        json_result = {'userid': row.key[1], 'club': row.key[0], 'gender': row.key[2], 'sentiment_score': row.value[0]}
        target_db[str(count)] = json_result
        count += 1
    return target_db

def count_male_club_user(source_db):
    map_fun = '''function(doc) {
        if(doc.gender == 'male'){
            emit(doc.club, doc.sentiment_score)
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

    db_name = 'club_gender_count_new'
    target_db = create_database(db_name)
    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        json_result = {'club': row.key, 'male_sentiment_score': row.value[0], 'male_count': row.value[1]}
        target_db[row.key] = json_result
    return target_db

def add_female_club_user(source_db, target_db):
    map_fun = '''function(doc) {
        if(doc.gender == 'female'){
            emit(doc.club, doc.sentiment_score)
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

    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        print row
        document = target_db[row.key]
        document['female_sentiment_score'] = row.value[0]
        document['female_count'] = row.value[1]
        target_db.save(document)

def count_shopping_male_user(source_db):
    map_fun = '''function(doc) {
        if(doc.gender == 'male'){
            emit([doc.user.id, doc.gender], doc.sentiment_score)
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

    count = 0
    sum_of_sentiment = 0
    for row in source_db.query(map_fun, reduce_fun, group=True).rows:
        print row
        sum_of_sentiment += row.value[0]
        count += 1
    if count != 0:
        db_name = 'shopping_gender_count_new'
        target_db = create_database(db_name)
        json_result = {'count': count, 'sentiment_score': sum_of_sentiment / count}
        target_db['male'] = json_result
    return target_db

def add_shopping_female_user(source_db1, source_db2):
    map_fun = '''function(doc) {
        if(doc.gender == 'female'){
            emit([doc.user.id, doc.gender], doc.sentiment_score)
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

    count = 0
    sum_of_sentiment = 0
    for row in source_db1.query(map_fun, reduce_fun, group=True).rows:
        sum_of_sentiment += row.value[0]
        count += 1
    if count != 0:
        json_result = {'count': count, 'sentiment_score': sum_of_sentiment / count}
        source_db2['female'] = json_result

def create_database(name):
	couch = couchdb.Server('http://115.146.89.193:5984/')
	couch.resource.credentials = ('wppaul', 'qwert12345')
	try:
		target_database = couch.create(name)
	except couchdb.http.PreconditionFailed as e:
		del couch[name]
		target_database = couch.create(name)
	return target_database


couch = couchdb.Server('http://115.146.89.191:5984/')
# couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	source_database1 = couch.create('all_clubs_new')
except couchdb.http.PreconditionFailed as e:
	source_database1 = couch['all_clubs_new']

couch = couchdb.Server('http://115.146.89.191:5984/')
couch.resource.credentials = ('wppaul', 'qwert12345')
try:
    source_database2 = couch.create('shopping_new')
except couchdb.http.PreconditionFailed as e:
    source_database2 = couch['shopping_new']

tar_db1 = find_club_user(source_database1)
tar_db2 = count_male_club_user(tar_db1)
add_female_club_user(tar_db1, tar_db2)
tar_db3 = count_shopping_male_user(source_database2)
add_shopping_female_user(source_database2, tar_db3)


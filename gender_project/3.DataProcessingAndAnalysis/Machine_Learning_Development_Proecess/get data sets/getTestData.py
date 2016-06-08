# encoding=utf8  
import sys 
import re
import json
import couchdb
from facepp import API
from facepp import File
from genderizer.genderizer import Genderizer

reload(sys)  
sys.setdefaultencoding('utf8')

SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = '357e1ba0b55c577965c516d65f803501'
API_SECRET = 'xZKTRTcuFY5FEw1_TQFq7DW0I02ObSZo'

api = API(API_KEY,API_SECRET,SERVER)

def identify_gender(name):
    gender = Genderizer.detect(firstName = name)
    return gender

def get_face(newurl):
    try:
        face = api.detection.detect(url = newurl, mode='oneface')
        if not face['face']:
            return "NoResult"
        else:
            if face['face'][0]['attribute']['gender']['value'] == 'Female':
                return face['face'][0]['attribute']['gender']['confidence'] / 100
            else:
                return 1 - face['face'][0]['attribute']['gender']['confidence'] / 100
    except Exception as e:
        pass
        return "NoResult"

couch = couchdb.Server('http://115.146.89.67:5984')
# couch.resource.credentials = ('wppaul', 'qwert12345')
try:
	database = couch.create('melbourne_ccc')
except couchdb.http.PreconditionFailed as e:
	database = couch['melbourne_ccc']

male_count = 0
female_count = 0
male_count1 = 0
female_count1 = 0
male_ids = {}
female_ids = {}
output = open('test.txt', 'w')
output1 = open('train_prob.txt', 'w')
f = open('ids.txt', 'r').read()
ids = f.split('\n')
image_url = {}

for id in database:
	if int(id) >= 600001076985597952:
		data = database[str(id)]
		if data['lang'] == 'en' and data['user']['id'] != None and data['user']['id'] not in ids:
			gender = identify_gender(data['user']['name'].split(' ', 1)[0])

			if gender != None and data['user']['profile_image_url'] != None and data['user']['default_profile_image'] == False:
				profile_image = re.sub('_normal', '', data['user']['profile_image_url'])
				if profile_image not in image_url:
					try:
						results = get_face(profile_image)
						# print results
					except Exception as e:
						print e
						time.sleep(10)
						results = get_face(profile_image)
					image_url[profile_image] = results
				else:
					results = image_url[profile_image]

				if results != 'NoResult' and gender == 'male' and male_count < 5000:
					if data['user']['id'] not in male_ids:
						male_ids[data['user']['id']] = 0
					else:
						male_ids[data['user']['id']] += 1
				elif results != 'NoResult' and gender == 'female' and female_count < 5000:
					if data['user']['id'] not in female_ids:
						female_ids[data['user']['id']] = 0
					else:
						female_ids[data['user']['id']] += 1

				if results != 'NoResult' and gender == 'male' and male_count < 5000 and male_ids[data['user']['id']] < 8:
					output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(gender, data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
					# ids.append(data['user']['id'])
					print male_count, str(id)
					male_count += 1
				elif results != 'NoResult' and gender == 'female' and female_count < 5000 and female_ids[data['user']['id']] < 8:
					output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(gender, data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
					# ids.append(data['user']['id'])
					print female_count, str(id)
					female_count += 1
				elif results != 'NoResult' and gender == 'male' and male_count == 5000 and data['user']['id'] not in male_ids and male_count1 < 10000:
					output1.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(gender, data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
					print male_count1, str(id)
					male_count1 += 1
				elif results != 'NoResult' and gender == 'female' and female_count == 5000 and data['user']['id'] not in female_ids and female_count1 < 10000:
					output1.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(gender, data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
					print female_count1, str(id)
					female_count1 += 1
				elif male_count1 == 10000 and female_count1 == 10000:
					print 'finish'
					break


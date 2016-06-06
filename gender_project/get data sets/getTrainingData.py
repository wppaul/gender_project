# encoding=utf8  
import sys 
import re
import json
import couchdb
from facepp import API
from facepp import File

reload(sys)  
sys.setdefaultencoding('utf8')

SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = '7444b6cbcb6c3381309542816ff26e32'
API_SECRET = 'XAXI-zZ13p0HBctYX5M_kxe2xutu_E7n'

api = API(API_KEY,API_SECRET,SERVER)

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

couch = couchdb.Server('http://115.146.89.191:5984')
try:
	database = couch.create('melbourne_tweets')
except couchdb.http.PreconditionFailed as e:
	database = couch['melbourne_tweets']

male_count = 0
female_count = 0
output = open('output1.txt', 'w')

image_url = {}
for id in database:
	if int(id) > 710000469494644736:
		data = database[str(id)]
		if data['gender'] == 'male' and data['lang'] == 'en' and data['user']['id'] != None and data['user']['profile_image_url'] != None and data['user']['default_profile_image'] == False:

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

			if results != 'NoResult' and results <= 0.5:
				print(str(id), 'male success', str(male_count))
				male_count+=1
				output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(data['gender'], data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
			else:
				print(str(id) + ': inconsistent with: ' + data['gender'] + ': ' + str(results))

		elif data['gender'] == 'female' and data['lang'] == 'en' and data['user']['id'] != None and data['user']['profile_image_url'] != None and data['user']['default_profile_image'] == False:

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

			if results != 'NoResult' and results > 0.5:
				print(str(id), 'female success', str(female_count))
				female_count+=1
				output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(data['gender'], data['text'].replace('\n', ' '), data['user']['description'], profile_image, results, data['user']['id']))
			else:
				print(str(id) + ': inconsistent with: ' + data['gender'] + ': ' + str(results))


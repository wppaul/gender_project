# encoding=utf8  

import tweepy
import socket
import requests
import time
from authentication2 import authentication  # Consumer and access token/key
import sys 
import json
import googlemaps

reload(sys)  
sys.setdefaultencoding('utf8')

class TwitterStreamListener(tweepy.StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.
	"""

	def __init__(self, api=None):
		super(TwitterStreamListener, self).__init__()
		self.num_tweets = 0
		self.total = 0

	def on_status(self, status):
		
		if self.num_tweets < 2500:

			if status.user.name != None and status.user.profile_image_url_https != None and status.text != None and status.place != None and status.place.full_name == "Melbourne, Victoria":
			
				self.total += 1
				print self.total, ':', status.id
				json_result = status._json

				if status.coordinates != None:
					self.num_tweets += 1

					print(status.coordinates["coordinates"])
					lat = status.coordinates["coordinates"][1]
					lon = status.coordinates["coordinates"][0]
					suburb = ""
					postal_code = ""
					reverse_geocode_result = gmaps.reverse_geocode((lat,lon))
					for each in reverse_geocode_result:
						for one in each['address_components']:
							if suburb == "" or postal_code == "":
								if one['types'] == ['locality', 'political']:
									print(one['long_name'])
									suburb = one['long_name']
								if one['types'] == ['postal_code']:
									print(one['long_name'])
									postal_code = one['long_name']
					if suburb != "" and postal_code != "":
						json_result['suburb'] = suburb
						json_result['postal_code'] = postal_code
						json_result['has_coor'] = 'True'
						# print(json_result)
					else:
						json_result['suburb'] = ""
						json_result['postal_code'] = '0000'
						json_result['has_coor'] = 'False'
				else:
					json_result['suburb'] = ""
					json_result['postal_code'] = '0000'
					json_result['has_coor'] = 'False'

				return True
		else:
			return False

	# Twitter error list : https://dev.twitter.com/overview/api/response-codes
	
	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			print('out of limit')
	
	
if __name__ == '__main__':
	print('begin')

	# Get access and key from another class
	auth = authentication()

	consumer_key = auth.getconsumer_key()
	consumer_secret = auth.getconsumer_secret()

	access_token = auth.getaccess_token()
	access_token_secret = auth.getaccess_token_secret()

	gmaps = googlemaps.Client(key='AIzaSyCGwI22mO3khzq1_cttVxoBTK_auzfWEjI')

	# Authentication
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.secure = True
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
	streamListener = TwitterStreamListener()
	myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
	# terms = ['Melbourne']
	myStream.filter(locations = [144.593742, -38.433859,145.512529, -37.511274], async=True)
#144.900004, -37.972567, 145.206266, -37.511274 
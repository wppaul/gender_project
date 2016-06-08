# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This scripts is used for real-time tweets collecting and boost tweets through user timeline search
# encoding=utf8 

import tweepy
import socket
import requests
import time
from authentication_e import authentication  # Consumer and access token/key
import sys 
import json
import googlemaps
import couchdb
from genderizer.genderizer import Genderizer
from textblob import TextBlob

reload(sys)  
sys.setdefaultencoding('utf8')

searched_list = []

# This function is adding gender to a tweet
def identify_gender(name):
    gender = Genderizer.detect(firstName = name)
    return gender
# This function is adding sentiment to a tweet
def add_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# This function is for getting tweets in user timeline
def get_timeline(user_name):
    tweetslist = []
    try:
        new_tweets = api.user_timeline(screen_name = user_name, count = 200, include_rts = True)
        tweetslist.extend(new_tweets)
        oldest = tweetslist[-1].id - 1
        
        # keep collecting tweets until there are no tweets left
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=user_name, count=200, max_id=oldest)
            tweetslist.extend(new_tweets)
            oldest = tweetslist[-1].id - 1
    except tweepy.TweepError:
        print("Time out or wait!!!")
        pass
    except IndexError:
        return tweetslist
    except Exception as e:
        print ("---Encountered Exception userAllTweet: ", e)
    return tweetslist
# This function is checking whether the tweet meets the requirements
def check_requirements(tweet):
    if tweet["user"]["name"] != None and tweet["user"]["profile_image_url_https"] != None and tweet["text"] != None and tweet["place"] != None and tweet["place"]["full_name"] == "Melbourne, Victoria":
        return True
    else:
        return False

# This function is checking whether the user name is in the searched list
def check_searched_name(user_name):
    notexist = user_name not in searched_list
    if notexist:
       searched_list.append(user_name)
       with open('/home/ubuntu/streaming_with_timeline_search/searched_list.txt','a') as f:
           f.write(user_name + "\n")
           return True
    else:
        return False
# This function is adding extra features to the raw tweets such gender,sentiment score
def processing_tweets(raw_tweets):
    jsontweets = raw_tweets
    first_name = jsontweets['user']['name'].split(' ', 1)[0]
    jsontweets['gender'] = identify_gender(first_name)
    jsontweets['sentiment_score'] = add_sentiment(jsontweets['text'])
    jsontweets['has_coor'] ='needcheck'
    return jsontweets

# This function is saving the processed tweets to couchdb
def save_to_database(raw_tweets):
    jsontweets = raw_tweets
    try:
        if jsontweets['id_str'] not in data_base:
            processedtweets = processing_tweets(jsontweets)
            data_base[jsontweets['id_str']] = processedtweets
    except Exception as e:
        print(("Oops,something wrong with saving the tweet:", e))
        pass
    return True

class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, api=None):
        super(TwitterStreamListener, self).__init__()
        self.num_tweets = 0
        self.total = 0

    def on_status(self, status):
        if check_requirements(status._json) == True:
            save_to_database(status._json)
            username = status._json['user']['screen_name']
            if check_searched_name(username) == True: # if user screen name is not in the list then search timeline to get more tweets
                incomingtweets = get_timeline(username)
                for tweets in incomingtweets:
                    if check_requirements(tweets._json) == True:
                        save_to_database(tweets._json)
            else:
                print ("already searched!!")
                    
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
 
    # create and connect to database
    couch = couchdb.Server('http://localhost:5984/')
    try:
        data_base = couch.create('melbourne_tweets')
    except couchdb.http.PreconditionFailed as e:
        data_base = couch['melbourne_tweets']
    
    # read the searched list
    with open('/home/ubuntu/streaming_with_timeline_search/searched_list.txt','r') as f:
        for line in f.readlines():
            searched_list.append(line.strip('\n'))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    streamListener = TwitterStreamListener()

    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    myStream.filter(locations = [144.593742, -38.433859,145.512529, -37.511274], async=True) 





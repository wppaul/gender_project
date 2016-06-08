# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This scripts is used for searching tweets based on related keywords

import sys
import tweepy
import time
import json
import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from genderizer.genderizer import Genderizer
from textblob import TextBlob

reload(sys)
sys.setdefaultencoding('utf8')
#print(sys.getdefaultencoding())

CONSUMER_KEY = 'CWaCe1cSVZ52vhuAMpDpL7BUe'
CONSUMER_SECRET = 'JnJuiQicmBgNF97mq3XLNNhdKg5S6leA0Ff3iAuxTj4YnbwitL'
# ACCESS_TOKEN = '2781913309-qBuhr8kA7OeaBO4aAYiYDD71JgWfPBd0MChgWkO'
# ACCESS_TOKEN_SECRET = 'CqAqs0ccGiO4YWcgVoBypk4E6KNPpv1Om9IqtkMvjp0KX'
# auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

# App auth allows 450 requests other than 180 with user auth 
auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

api = tweepy.API(auth)

# This function is checking whether the tweet meets the requirements
def check_requirements(tweet):
    if tweet["user"]["name"] != None and tweet["user"]["profile_image_url_https"] != None and tweet["text"] != None and tweet["place"] != None and tweet["place"]["full_name"] == "Melbourne, Victoria":
        return True
    else:
        return False
# This function is adding gender to a tweet
def identify_gender(name):
    gender = Genderizer.detect(firstName = name)
    return gender
# This function is adding sentiment to a tweet
def add_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

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

if __name__ == '__main__':

    my_list = ['AFL','footy']
    if(api.verify_credentials):
        print 'We sucessfully logged in, start collecting'

        # create and connect to database
    couch = couchdb.Server('http://localhost:5984/')
    try:
        data_base = couch.create('melbourne_tweets')
    except couchdb.http.PreconditionFailed as e:
        data_base = couch['melbourne_tweets']

    new_tweets = tweepy.Cursor(api.search,
                           count=100,
                           q=my_list,
                           result_type='recent',
                           include_entities=True,
                           monitor_rate_limit=True, 
                           wait_on_rate_limit=True,
                           geocode="-37.694571,144.711350,46km").pages()
    while True:
        try:
            tweets_on_page = next(new_tweets)
            for status in tweets_on_page:
                if check_requirements(status._json) == True:
                    print status._json['id_str']
                    save_to_database(status._json)
        except tweepy.TweepError:
            print 'Time out,please wait!!!'
            continue
        except StopIteration:
            print 'no more new tweets found!'
            break
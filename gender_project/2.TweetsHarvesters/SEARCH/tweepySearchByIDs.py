# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This scripts is used for searching tweets based on followers' IDs

import sys
import os
import tweepy
import time
import json
import couchdb
from genderizer.genderizer import Genderizer
from textblob import TextBlob
import argparse

reload(sys)
sys.setdefaultencoding('utf8')

user_id_list = []
searched_list =[]
couch_ip = 'http://localhost:5984/'

def get_timeline(user_id):
    tweetslist = []
    try:
        new_tweets = api.user_timeline(user_id = user_id, count = 200, include_rts = True)
        tweetslist.extend(new_tweets)
        oldest = tweetslist[-1].id - 1
        
        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(user_id=user_id, count=200, max_id=oldest)
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

# This function is adding gender to a tweet
def identify_gender(name):
    gender = Genderizer.detect(firstName = name)
    return gender

# This function is adding sentiment to a tweet
def add_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def check_searched_id(user_id):
    notexist = user_id not in searched_list
    if notexist:
       searched_list.append(user_id)
       with open(searched_file_path,'a') as f:
           f.write(user_id + "\n")
           return True
    else:
        return False

# This function is adding extra features to the raw tweets such gender,sentiment score
def processing_tweets(raw_tweets):
    jsontweets = raw_tweets
    first_name = jsontweets['user']['name'].split(' ', 1)[0]
    jsontweets['gender'] = identify_gender(first_name)
    jsontweets['sentiment_score'] = add_sentiment(jsontweets['text'])
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

    CONSUMER_KEY = 'l69z6yj3QLLayxnqKT5aiKmXE'
    CONSUMER_SECRET = 'uh1y8C8kjhgUoxP7snicfsPctdclHQETCLhvAh5ejf71mszJgG'
    ACCESS_TOKEN = '3181028461-tOaBc8xmSnmOrSfRWqyOJuxcDAMuEaKQrVFYpgO'
    ACCESS_TOKEN_SECRET = '1GlIDZnD1StVcJqb1mOF6EYGY0V5Ienddoeg2lLiNJ5cY'


    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))

    if(api.verify_credentials):
        print 'We sucessfully logged in, start searching'

    parser = argparse.ArgumentParser(description='You need Three Arguments!!')
    parser.add_argument('-l', action="store",dest="user_list_file_path", type=str)
    parser.add_argument('-s', action="store",dest="searched_file_path", type=str)
    parser.add_argument('-d', action="store",dest="data_base_name", type=str)

    user_list_file_path = parser.parse_args().user_list_file_path
    searched_file_path = parser.parse_args().searched_file_path
    data_base_name = parser.parse_args().data_base_name

    # create and connect to database
    couch = couchdb.Server(couch_ip)
    try:
        data_base = couch.create(data_base_name)
    except couchdb.http.PreconditionFailed as e:
        data_base = couch[data_base_name]

    with open(user_list_file_path,'r') as f:
        for line in f.readlines():
            user_id_list.append(line.strip('\n'))

    with open(searched_file_path,'r') as f:
        for line in f.readlines():
            searched_list.append(line.strip('\n'))

    for user_id in user_id_list:
        if check_searched_id(user_id) == True:
            incomingtweets = get_timeline(user_id)
            for tweets in incomingtweets:
                if check_requirements(tweets._json) == True:
                    save_to_database(tweets._json)
        else:
            print ("already searched!!")
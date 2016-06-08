# Author :  PENG WANG          MINGYU GAO
# Student Number : 680868      692634
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This scripts is used for get followers' IDs from target Offical Account such as AFL Clubs
# encoding=utf8
import sys
import tweepy
import time
import json
import couchdb
from genderizer.genderizer import Genderizer
import argparse

reload(sys)
sys.setdefaultencoding('utf8')

def get_ids(target_name):
    target_name = target_name
    user_id = tweepy.Cursor(api.followers_ids, screen_name=target_name).pages()
    while True:
        try:
            pages = next(user_id)
            with open('%s'%target_name,'a') as f:
                f.write("\n".join(str(x) for x in pages))
                f.write("\n")

        except tweepy.TweepError:
            print ('We got a timeout ... Sleeping for 15 minutes')
            time.sleep(15*60)
            continue
        except StopIteration:
            print ("got all the results!")
            break

if __name__ == '__main__':
    
    CONSUMER_KEY = 'U6AFxW70cGkl95SHhXN0wBFHD'
    CONSUMER_SECRET = 'xdQA50Ld52aBdyu8bWPXynugVKf3dTkhF3nT2i4gtiFWY6Fsmo'
    auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    api = tweepy.API(auth)
    if(api.verify_credentials):
        print 'We sucessfully logged in, start collecting'
    parser = argparse.ArgumentParser(description='Please Type a Offical Account Name!')
    parser.add_argument('-n', action="store",dest="name", type=str)
    target_name = parser.parse_args().name
    get_ids(target_name)

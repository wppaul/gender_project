 # encoding=utf8
import sys
import tweepy
import time
import json
import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from genderizer.genderizer import Genderizer

reload(sys)
sys.setdefaultencoding('utf8')

CONSUMER_KEY = 'U6AFxW70cGkl95SHhXN0wBFHD'
CONSUMER_SECRET = 'xdQA50Ld52aBdyu8bWPXynugVKf3dTkhF3nT2i4gtiFWY6Fsmo'
ACCESS_TOKEN = '2781643920-le1wXn3e3YGxtdujK8i2F1VWxgLV11Vv7C9kIk2'
ACCESS_TOKEN_SECRET = '5TAZszMTilSgyKUjwwNWMdmfBSq0mXwovQuW4Zy5K7Wrl'

# auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

api = tweepy.API(auth)

if(api.verify_credentials):
    print 'We sucessfully logged in, start collecting'

# stuff = api.user_timeline(user_id = '720864247983448064', count = 200, include_rts = True)

# print stuff[0]._json['user']['statuses_count'] > 10
# for status in stuff:
#     print status._json

# ids = []

user_id = tweepy.Cursor(api.followers_ids, screen_name='AFL').pages()

# # count = 0
while True:
    try:
        pages = next(user_id)
        with open('/Users/Paul/desktop/stkildafc.txt','a') as f:
            f.write("\n".join(str(x) for x in pages))
            f.write("\n")
        # count+=1
        # time.sleep(60)
    except tweepy.TweepError:
        print ('We got a timeout ... Sleeping for 15 minutes')
        time.sleep(15*60)
        continue
    except StopIteration:
        print ("got all the results!")
        break
    # except:
    # 	print 'We got a timeout ... Sleeping for 15 minutes'
        # time.sleep(15*60)
        # pages = next(user_id)
        # with open('/Users/Paul/desktop/ess_id.txt','a') as f:
        #     f.write("\n".join(str(x) for x in pages))
print api.rate_limit_status()['resources']['followers']['/followers/ids']
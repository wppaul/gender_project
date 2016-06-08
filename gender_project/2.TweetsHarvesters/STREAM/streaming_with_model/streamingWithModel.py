# Author :  PENG WANG          MINGYU GAO
# Student Number : 680868      692634
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This scripts is used for real-time tweets collecting together with gender prediction
# encoding=utf8 
import tweepy
import socket
import requests
import time
from authentication import authentication  # Consumer and access token/key
import sys 
import json
import googlemaps
import couchdb
import smtplib
import datetime
from genderizer.genderizer import Genderizer
from textblob import TextBlob
import nltk
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from collections import defaultdict
from facepp import API
from facepp import File

reload(sys)  
sys.setdefaultencoding('utf8')

class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, api=None):
        super(TwitterStreamListener, self).__init__()
        self.startTime = datetime.datetime.now()
        self.num_tweets = 0
        self.total = 0

    def on_status(self, status):
        
        if self.num_tweets < 2500:
            if len(image_url) >= 10000:
                image_url = {}
            if len(user) >= 10000:
                user = defaultdict(list)
            if datetime.datetime.now() - startTime > datetime.timedelta(hour=24):
                self.startTime = datetime.datetime.now()
                self.num_tweets = 0
            if status.user.name != None and status.user.profile_image_url_https != None and status.text != None and status.place != None and status.place.full_name == "Melbourne, Victoria":
                if status.id_str not in data_base:
                    self.total += 1
                    json_result = status._json
                    userid = status.user.id
                    first_name = status.user.name.split(' ', 1)[0]
                    text = status.text
                    description = status.user.description
                    image = status.user.profile_image_url
                    default = status.user.default_profile_image

                    #Add Sentiment Score
                    json_result['sentiment_score'] = add_sentiment(text)

                    #Add Suburb and Postcode
                    if status.coordinates != None:
                        self.num_tweets += 1

                        lat = status.coordinates["coordinates"][1]
                        lon = status.coordinates["coordinates"][0]
                        suburb = ""
                        postal_code = ""
                        reverse_geocode_result = gmaps.reverse_geocode((lat,lon))
                        for each in reverse_geocode_result:
                            for one in each['address_components']:
                                if suburb == "" or postal_code == "":
                                    if one['types'] == ['locality', 'political']:
                                        suburb = one['long_name']
                                    if one['types'] == ['postal_code']:
                                        postal_code = one['long_name']
                        if suburb != "" and postal_code != "":
                            json_result['suburb'] = suburb
                            json_result['postal_code'] = postal_code
                            json_result['has_coor'] = 'True'
                        else:
                            json_result['suburb'] = ""
                            json_result['postal_code'] = '0000'
                            json_result['has_coor'] = 'False'
                    else:
                        json_result['suburb'] = ""
                        json_result['postal_code'] = '0000'
                        json_result['has_coor'] = 'False'

                    #Add Gender
                    gender = identify_gender(first_name)
                    if gender == 'male' or gender == 'female':
                        json_result['gender'] = gender
                    else:
                        if len(user[userid]) < 5:
                            if default == False and image != None:
                                profile_image = re.sub('_normal', '', image)
                                if profile_image not in image_url:
                                    try:
                                        face_results = get_face(profile_image)
                                    except Exception as e:
                                        print e
                                        time.sleep(10)
                                        face_results = get_face(profile_image)
                                    image_url[profile_image] = face_results
                                else:
                                    face_results = image_url[profile_image]
                            else:
                                face_results = 0.5

                            if text != None:
                                prob_text = predict_bow(text, vectorizer_text, clf_text)
                            else:
                                prob_text = 0.5

                            if description != None:
                                prob_description = predict_bow(description, vectorizer_description, clf_description)
                            else:
                                prob_description = 0.5

                            gender = clf_prob.predict([[prob_text,prob_description,face_results]])[0]
                            user[userid].append(gender)

                        else:
                            male_count = 0
                            female_count = 0
                            for each in user[userid]:
                                if each == 'male':
                                    male_count += 1
                                else:
                                    female_count += 1
                            if male_count > female_count:
                                gender = 'male'
                            else:
                                gender = 'female'

                        json_result['gender'] = gender
                    
                    print self.total, ':', status.id, json_result['gender'], json_result['sentiment_score']
                    data_base[status.id_str] = json_result  #adding json to database
                    return True  
        else:
            notification('Google API is reaching the limit')
            return False

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            print('out of limit')


def notification(msg):
    FROM ="professional.bigdata@hotmail.com"
    TO =["wppaul@hotmail.com","edwardgao46@yahoo.com.au"]

    SUBJECT = "Google API is reaching the limit!!"
    TEXT = msg
    message = """Subject: %s\n
        %s
        """%(SUBJECT,TEXT)
    server = smtplib.SMTP('smtp-mail.outlook.com',port = 587)
    server.starttls()
    server.login('professional.bigdata@hotmail.com','professional@bigdata')
    server.sendmail(FROM,TO,message)
    server.quit()

def identify_gender(name):
    gender = Genderizer.detect(firstName = name)
    return gender

def add_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def filter_emoji(tweet):
    pattern = u'[\uD800-\uDBFF][\uDC00-\uDFFF]'
    emoji = re.findall(pattern, tweet)
    
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    des_tweet = co.sub('', tweet)
    return des_tweet, emoji

def preprocess_to_tokens(text):
    # remove noises
    text = re.sub(r'http\S+', '', text)
#     text = re.sub('@\w+ ?', '', text)
    text = re.sub('\s*[0-9]+\s*', '', text)
    
    # convert hashtags into words
    pattern = '#\w+'
    hashtag = re.findall(pattern, text)
    text = re.sub(pattern, '', text)
    global hashtagwords_temp
    hashtagwords = []
    for each in hashtag:
        hashtagwords_temp = []
        maxmatch(each[1:len(each)])
        if len(hashtagwords_temp) >= 3:
            hashtagwords.append(each)
        else:
            for each in hashtagwords_temp:
                hashtagwords.append(each)

    word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
    tokenized_sentence = word_tokenizer.tokenize(text)
    
    tokens = []
    
    for each in tokenized_sentence:
        each = re.sub('\W', '', lemmatize(each.lower()))
        if each != '':
            tokens.append(each)
        
    for each in hashtagwords:
        tokens.append(lemmatize(each.lower()))

    return tokens

def lemmatize(word):
    lemma = lemmatizer.lemmatize(word,'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')
    return lemma

def maxmatch(word):
    for i in range(0, len(word)):
        if word[0:1] in wordSet:
            lemma_word = lemmatize(word[0:(len(word) - i)].lower())
            if lemma_word in wordSet:
                hashtagwords_temp.append(lemma_word)
                word = word[(len(word) - i) : len(word)]
                maxmatch(word)
                break
        else:
            word = word[1 : len(word)]
            maxmatch(word)
            break
            
def get_unigram_BOW(tokens):
    BOW = {}
    for word in tokens:
        if word not in stopwords:
            BOW[word] = BOW.get(word,0) + 1
    return BOW

def get_bigrams_BOW(tokens):
    BOW = {}
    for word in tokens:
        if word not in stopwords:
            BOW[word] = BOW.get(word,0) + 1
    if len(tokens) > 1:
        for i in range(0,len(tokens) - 1):
            BOW[tokens[i] + ' ' + tokens[i+1]] = BOW.get(tokens[i] + ' ' + tokens[i+1], 0) + 1
    return BOW

def prepare_bow_set(filename, feature_extractor):
    training_set = []
    training_classifications = []
    training_set_bow = []

    f = open(filename, "r").read()
    rows = f.split('\n')
    pairs = []
    for row in rows:
        pairs.append(row.split('\t'))
        
    #Prepare for calculating the frequency of every word
    for pair in pairs:
        if len(pair) == 2:
            des_tweet, emoji = filter_emoji(pair[1].decode('utf-8'))
            pro_tweet = preprocess_to_tokens(des_tweet)
            for each in emoji:
                pro_tweet.append('iamemoji')
            bow = feature_extractor(pro_tweet)
            if len(bow) != 0:
                training_set.append(bow)

    #remove all words that appear only once
    for text in training_set:
        for token in text:
            frequency[token] += 1
    for pair in pairs:
        if len(pair) == 2:
            des_tweet, emoji = filter_emoji(pair[1].decode('utf-8'))
            pro_tweet = preprocess_to_tokens(des_tweet)
            for each in emoji:
                pro_tweet.append(each)
            temp = feature_extractor(pro_tweet)
            bow = {}
            if len(temp) != 0:
                for each in temp:
                    if frequency[each] > 0 or each not in frequency:
                        bow[each] = temp[each]
            if len(bow) != 0:
                training_set_bow.append(bow)
                training_classifications.append(pair[0])
    
    vectorizer = DictVectorizer().fit(training_set_bow)

    print "Transforming Text into Bow Features..."
    training_data_bow = vectorizer.transform(training_set_bow)
    print(training_data_bow.shape)
    return training_data_bow,training_classifications,vectorizer

def prepare_bow_set_des(filename, feature_extractor):
    training_set = []
    training_classifications = []
    training_set_bow = []

    f = open(filename, "r").read()
    rows = f.split('\n')
    pairs = []
    for row in rows:
        pairs.append(row.split('\t'))
        
    #Prepare for calculating the frequency of every word
    for pair in pairs:
        if len(pair) == 2:
            des_tweet, emoji = filter_emoji(pair[1].decode('utf-8'))
            pro_tweet = preprocess_to_tokens(des_tweet)
            for each in emoji:
                pro_tweet.append('iamemoji')
            bow = feature_extractor(pro_tweet)
            if len(bow) != 0:
                training_set.append(bow)

    #remove all words that appear only once
    for text in training_set:
        for token in text:
            frequency[token] += 1
    for pair in pairs:
        if len(pair) == 2:
            des_tweet, emoji = filter_emoji(pair[1].decode('utf-8'))
            pro_tweet = preprocess_to_tokens(des_tweet)
            for each in emoji:
                pro_tweet.append(each)
            temp = feature_extractor(pro_tweet)
            bow = {}
            if len(temp) != 0:
                for each in temp:
                    if frequency[each] > 0 or each not in frequency:
                        bow[each] = temp[each]
            if len(bow) != 0:
                training_set_bow.append(bow)
                training_classifications.append(pair[0])
    
    vectorizer = DictVectorizer().fit(training_set_bow)

    print "Transforming Description into BoW Features..."
    training_data_bow = vectorizer.transform(training_set_bow)
    print(training_data_bow.shape)
    return training_data_bow,training_classifications,vectorizer

def predict_bow(text, feature_extractor, vectorizer, clf):
    raw, emoji = filter_emoji(text)
    atext = preprocess_to_tokens(raw)
    for each in emoji:
        atext.append(each)
    bow = feature_extractor(atext)
    if len(bow) != 0:
        vectorizer.transform(bow)
        return clf.predict_proba(vectorizer.transform(bow))[0][0]
    else:
        return 0.5
    
def prepare_combined_model(clf_text, clf_description, vectorizer_text, vectorizer_description, prob_fname):
    print 'Preparing Combined Model...'
    f = open(prob_fname, "r").read()
    rows = f.split('\n')
    pairs = []
    testset = []
    test_prob = []
    test_class = []
    
    for row in rows:
        pairs.append(row.split('\t'))
    for pair in pairs:
        if len(pair) == 6:
            testset.append(pair)    

    for each in testset:
        # if len(each[1]) >= 25:
        prob_text = predict_bow(each[1].decode('utf-8'), get_bigrams_BOW, vectorizer_text, clf_text)
        prob_description = predict_bow(each[2].decode('utf-8'), get_bigrams_BOW, vectorizer_description, clf_description)
        prob_image = float(each[4]) - (float(each[4]) - 0.5)/2
        test_prob.append([prob_text, prob_description, prob_image])
        test_class.append(each[0])

    return test_prob, test_class
    
def get_face(newurl):
    try:
        face = facepp_api.detection.detect(url = newurl, mode='oneface')
        if not face['face']:
            return 0.5
        else:
            if face['face'][0]['attribute']['gender']['value'] == 'Female':
                p = float(face['face'][0]['attribute']['gender']['confidence'] / 100)
            else:
                p = float(1 - face['face'][0]['attribute']['gender']['confidence'] / 100)
            return p - (p - 0.5) / 2
    except Exception as e:
        pass
        return 0.5

def get_gender(prob):
    if prob > 0.5:
        return 'female'
    else:
        return 'male'
    
def connect_couchdb(ip, db_name):
    couch = couchdb.Server(ip)
#     couch.resource.credentials = ('wppaul', 'qwert12345')
    try:
        database = couch.create(db_name)
    except couchdb.http.PreconditionFailed as e:
        database = couch[db_name]
    return database

    
if __name__ == '__main__':
    # Get access and key from another class
    auth = authentication()

    consumer_key = auth.getconsumer_key()
    consumer_secret = auth.getconsumer_secret()
    access_token = auth.getaccess_token()
    access_token_secret = auth.getaccess_token_secret()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    #Connect Google Maps API
    gmaps = googlemaps.Client(key='AIzaSyCGwI22mO3khzq1_cttVxoBTK_auzfWEjI')

    #Connect Face++ API
    SERVER = 'http://api.us.faceplusplus.com/'
    API_KEY = '3a7092b400dc9827359d7093801f057d'
    API_SECRET = 'ChXgzhIEau8A1O_aKOanTS7dzY0AgVKQ'
    facepp_api = API(API_KEY,API_SECRET,SERVER)

    #Connect CouchDB
    print 'Connecting CouchDB...'
    data_base = connect_couchdb('http://115.146.89.191:5984/', 'melbourne_tweets_new')

    #Prepare for ML Models
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    wordSet = set(nltk.corpus.words.words())
    stopwords = set(nltk.corpus.stopwords.words('english'))
    hashtagwords_temp = []
    text_training_set = "training_text_final.txt"
    description_training_set = "training_description_final.txt"
    prob_training_set = "training_prob_final.txt"
    test_set = "test.txt"
    user = defaultdict(list)
    image_url = {}

    print 'Preparing Data Sets...'
    frequency = defaultdict(int)
    trn_text_bow, trn_text_classes_bow, vectorizer_text = prepare_bow_set(text_training_set, get_bigrams_BOW)
    frequency = defaultdict(int)
    trn_description_bow, trn_description_classes_bow, vectorizer_description = prepare_bow_set_des(description_training_set, get_bigrams_BOW)

    #Build Models
    print 'Builing Models...'
    clf_text = BernoulliNB(alpha = 0.17012542798525856, binarize=0.0, class_prior=None, fit_prior=True)
    clf_description = BernoulliNB(alpha=0.00062355073412739121, binarize=0.0, class_prior=None, fit_prior=True)
    clf_prob = LogisticRegression(C=1, class_weight='balanced', dual=False, fit_intercept=True, intercept_scaling=0.2, max_iter=100, multi_class='ovr', 
                                  n_jobs=1, penalty='l2', random_state=None, solver='liblinear', tol=0.0001, verbose=0, warm_start=False)

    #Fit Data Sets
    print 'Fitting Data Sets...'
    clf_text.fit(trn_text_bow,trn_text_classes_bow) 
    clf_description.fit(trn_description_bow,trn_description_classes_bow)
    trn_prob,trn_prob_class = prepare_combined_model(clf_text,clf_description,vectorizer_text,vectorizer_description,test_set)
    clf_prob.fit(trn_prob, trn_prob_class)

    #Listening the Streaming API
    print 'Begin Listening...'
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    # terms = ['Melbourne']
    myStream.filter(locations = [144.593742, -38.433859,145.512529, -37.511274], async=True)
    
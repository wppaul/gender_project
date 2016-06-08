
# coding: utf-8

# In[2]:


import nltk
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.metrics import accuracy_score, classification_report, roc_curve, roc_auc_score, auc, log_loss
import numpy as np
from collections import defaultdict
from facepp import API
from facepp import File
import time
import couchdb
from datetime import datetime
# import matplotlib.pyplot as plt

startTime = datetime.now()
    
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

def get_male_BOW(tokens):
    global male_BOW
    for word in tokens:
        if word not in stopwords:
            male_BOW[word] = male_BOW.get(word,0) + 1

def get_female_BOW(tokens):
    global female_BOW
    for word in tokens:
        if word not in stopwords:
            female_BOW[word] = female_BOW.get(word,0) + 1

def get_top_topic():
    top_male_words = sorted(male_BOW.iteritems(), key=lambda d:d[1], reverse = True)[0:10]
    for word, frequent in top_male_words: 
        print "%s %d" % (word, frequent)
    
    top_female_words = sorted(female_BOW.iteritems(), key=lambda d:d[1], reverse = True)[0:10]
    for word, frequent in top_female_words: 
        print "%s %d" % (word, frequent)

def get_top_distinct_topic():
    freq1 = {}
    for each in male_BOW:
        if female_BOW.has_key(each):
            freq1[each] = male_BOW[each] - female_BOW[each]
        else:
            freq1[each] = male_BOW[each]
    top_male_words = sorted(freq1.iteritems(), key=lambda d:d[1], reverse = True)[0:10]
    for word, frequent in top_male_words: 
        print "%s %d" % (word, frequent)
        
    freq2 = {}
    for each in female_BOW:
        if male_BOW.has_key(each):
            freq2[each] = female_BOW[each] - male_BOW[each]
        else:
            freq2[each] = female_BOW[each]
    top_female_words = sorted(freq2.iteritems(), key=lambda d:d[1], reverse = True)[0:11]
    for word, frequent in top_female_words: 
        print "%s %d" % (word, frequent)
        
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
#                 if pair[0] == 'male':
#                     get_male_BOW(pro_tweet)
#                 elif pair[0] == 'female':
#                     get_female_BOW(pro_tweet)
    
#     get_top_topic()
#     get_top_distinct_topic()
    
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
#                 if pair[0] == 'male':
#                     get_male_BOW(pro_tweet)
#                 elif pair[0] == 'female':
#                     get_female_BOW(pro_tweet)
    
#     get_top_topic()
#     get_top_distinct_topic()
    
    vectorizer = DictVectorizer().fit(training_set_bow)

    print "Transforming Description into BoW Features..."
    training_data_bow = vectorizer.transform(training_set_bow)
    print(training_data_bow.shape)
    return training_data_bow,training_classifications,vectorizer

def prepare_tfidf_set(filename):
    training_data_tfidf = []
    training_classifications_tfidf = []
    f = open(filename, "r").read()
    rows = f.split('\n')
    pairs = []
    for row in rows:
        pairs.append(row.split('\t'))
    for pair in pairs:
        if len(pair) == 2:
            training_classifications_tfidf.append(pair[0])
            training_data_tfidf.append(pair[1])
            
    #Apply tf-idf
    tfidf_vectorizer = TfidfVectorizer(
        min_df=1, # min count for relevant vocabulary
        max_features=None, 
        strip_accents='unicode',  
        analyzer='word', # features made of words
#         token_pattern=r'\w{2,}', # tokenize only words of 2+ chars
        tokenizer = preprocess_to_tokens,
        stop_words=stopwords, 
        ngram_range=(1, 1), 
        use_idf=1,
        smooth_idf=1,
        sublinear_tf=1)
    print "Transforming tfidf data..."
    training_data_tfidf = tfidf_vectorizer.fit_transform(training_data_tfidf)
    print training_data_tfidf.shape
    return training_data_tfidf, training_classifications_tfidf, tfidf_vectorizer


def tune_parameter(trn_data, trn_classes, model):
    #Find the best parameters
    print "Tuning the Parameter..."
    
    clfs = []
    
    #Logistic Regression
    if 'LogisticRegression' in model:
        param_grid = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000], 'class_weight':[None, 'balanced']}
        gs_lr = GridSearchCV(estimator=LogisticRegression(penalty='l2', dual=False, tol=0.0001, fit_intercept=True, 
                                                          intercept_scaling=0.2, solver='liblinear', random_state=None), 
                             param_grid = param_grid, cv=20)
        gs_lr.fit(trn_data, trn_classes)
        print 'The best C for LR is: ', gs_lr.best_params_
        clfs.append(LogisticRegression(C=gs_lr.best_params_['C'], class_weight=gs_lr.best_params_['class_weight'], 
                                       penalty='l2', dual=False, tol=0.0001, fit_intercept=True, intercept_scaling=0.2, 
                                       solver='liblinear', random_state=None))
    
    #SVC with kernel is linear
    if 'SVC' in model:
        params_space = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'class_weight':[None, 'balanced']}
        gs_svc = GridSearchCV(estimator=SVC(kernel='linear'), param_grid=params_space, n_jobs=-1, cv=20)
        gs_svc.fit(trn_data, trn_classes)        
        print 'The best C for SVC is: ', gs_svc.best_params_
        clfs.append(SVC(C=gs_lr.best_params_['C'], kernel='linear'))
    
    #LinearSVC
    if 'LinearSVC' in model:
        params_space = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000], 'class_weight':[None, 'balanced'], 
                        'loss': ['hinge', 'squared_hinge']}
        gs_svc = GridSearchCV(estimator=LinearSVC(dual=True, fit_intercept=True, intercept_scaling=1, multi_class='ovr', 
                                                  penalty='l2', random_state=None, tol=0.0001, verbose=0), 
                              param_grid=params_space, n_jobs=-1, cv=20)
        gs_svc.fit(trn_data, trn_classes)        
        print 'The best C for LinearSVC is: ', gs_svc.best_params_    
        clfs.append(LinearSVC(C=gs_svc.best_params_['C'], class_weight=gs_svc.best_params_['class_weight'], dual=True, 
                              fit_intercept=True, intercept_scaling=1, loss=gs_svc.best_params_['loss'], multi_class='ovr', 
                              penalty='l2', random_state=None, tol=0.0001, verbose=0))
    
    #MultinomialNB
    if 'MultinomialNB' in model:
        param_grid = {'alpha': np.logspace(-5, 0, 40)}
        gs_mnb = GridSearchCV(estimator=MultinomialNB(), 
                         param_grid = param_grid, cv=20)
        gs_mnb.fit(trn_data, trn_classes)
        print 'The best alpha for MultinomialNB is: ', gs_mnb.best_params_
        clfs.append(MultinomialNB(alpha=gs_mnb.best_params_['alpha']))
    
    #BernoulliNB
    if 'BernoulliNB' in model:
        param_grid = {'alpha': np.logspace(-5, 0, 40)}
        gs_bnb = GridSearchCV(estimator=BernoulliNB(), 
                         param_grid = param_grid, cv=20)
        gs_bnb.fit(trn_data, trn_classes)
        print 'The best alpha for BernoulliNB are: ', gs_bnb.best_params_  
        clfs.append(BernoulliNB(alpha=gs_bnb.best_params_['alpha'], binarize = 0.0))
  
    return clfs

def do_multiple_20foldcrossvalidation(clfs,data,classifications):
    print 'Doing 20 fold Cross Validation...'
    for clf in clfs:
        predictions = cross_validation.cross_val_predict(clf, data,classifications, cv=10)
        tp = []
        p = []
        for each in classifications:
            if each == 'male':
                tp.append(0)
            else:
                tp.append(1)
        for each in predictions:
            if each == 'male':
                p.append(0)
            else:
                p.append(1)
        print clf
        print "Accuracy:", accuracy_score(classifications,predictions)
        print classification_report(classifications,predictions)
        print 'AUC:', roc_auc_score(tp,p)      

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

def predict_tfidf(text, vectorizer, clf):
    if len(text) != 0:
        vectorizer.transform(text)
        return clf.predict_proba(vectorizer.transform(text))[0][0]
    else:
        return 0.5
    
def tune_combined_model(clf_text, clf_description, bow_or_tfidf_text, bow_or_tfidf_description, fname1, fname2, fname3):
    print 'Building combined model...'
    f = open(fname3, "r").read()
    rows = f.split('\n')
    pairs = []
    testset = []
    test_prob = []
    test_class = []
    count_correct1 = 0
    count_correct2 = 0
    count = 0
    global frequency
    predict_text = ''
    predict_description = ''
    
    for row in rows:
        pairs.append(row.split('\t'))
    for pair in pairs:
        if len(pair) == 6:
            testset.append(pair)    
    
    frequency = defaultdict(int)
    if bow_or_tfidf_text == 'bow':
        trn_text_bow, trn_text_classes_bow, vectorizer_text = prepare_bow_set(fname1, get_bigrams_BOW)
        clf_text.fit(trn_text_bow,trn_text_classes_bow) 
        predict_text = predict_bow
    else:
        trn_data_tfidf,trn_classes_tfidf = prepare_tfidf_set(fname1)
        clf_text.fit(trn_text_tfidf,trn_text_classes_tfidf)
        predict_text = predict_tfidf
    
    frequency = defaultdict(int)
    if bow_or_tfidf_description == 'bow':
        trn_description_bow, trn_description_classes_bow, vectorizer_description = prepare_bow_set_des(fname2, get_bigrams_BOW)
        clf_description.fit(trn_description_bow,trn_description_classes_bow)
        predict_description = predict_bow
    else:
        trn_description_tfidf,trn_description_classes_tfidf, vectorizer_description = prepare_tfidf_set(fname2)
        clf_description.fit(trn_description_tfidf,trn_description_classes_tfidf)
        predict_description = predict_tfidf
        
    for each in testset:
#         if len(each[1]) >= 100:
        prob_text = predict_text(each[1].decode('utf-8'), get_bigrams_BOW, vectorizer_text, clf_text)
        prob_description = predict_description(each[2].decode('utf-8'), get_bigrams_BOW, vectorizer_description, clf_description)
        prob_image = float(each[4]) - (float(each[4]) - 0.5)/2
        test_prob.append([prob_text, prob_description, prob_image])
        test_class.append(each[0])

    clfs = tune_parameter(test_prob,test_class, ['LogisticRegression'])
    do_multiple_20foldcrossvalidation(clfs,test_prob,test_class)
    return clfs[0], test_prob, test_class
    
def prepare_combined_model(clf_text, clf_description, vectorizer_text, vectorizer_description, prob_fname):
    print 'Preparing combined model...'
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
        if len(each[1]) >= 25:
            prob_text = predict_bow(each[1].decode('utf-8'), get_bigrams_BOW, vectorizer_text, clf_text)
            prob_description = predict_bow(each[2].decode('utf-8'), get_bigrams_BOW, vectorizer_description, clf_description)
            prob_image = float(each[4]) - (float(each[4]) - 0.5)/2
            test_prob.append([prob_text, prob_description, prob_image])
            test_class.append(each[0])

    return test_prob, test_class
    
def get_face(newurl):
    try:
        face = api.detection.detect(url = newurl, mode='oneface')
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
        
#Connect CouchDB
database = connect_couchdb('http://115.146.89.191:5984/', 'melbourne_tweets_new')

#Connect Face++ API
SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = 'ab7428d1948018d0c81dbb6b3f38723d'
API_SECRET = 'e8BbAh7Wgg5pfJ8WSMcfhH-iAmad0AAF'
api = API(API_KEY,API_SECRET,SERVER)

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
wordSet = set(nltk.corpus.words.words())
stopwords = set(nltk.corpus.stopwords.words('english'))
hashtagwords_temp = []
text_training_set = "training_text_final.txt"
description_training_set = "training_description_final.txt"
prob_training_set = "training_prob_final.txt"
test_set = "test.txt"
male_BOW = {}
female_BOW = {}

frequency = defaultdict(int)
trn_text_bow, trn_text_classes_bow, vectorizer_text = prepare_bow_set(text_training_set, get_bigrams_BOW)
frequency = defaultdict(int)
trn_description_bow,trn_description_classes_bow,vectorizer_description=prepare_bow_set_des(description_training_set,get_bigrams_BOW)

clf_text = BernoulliNB(alpha = 0.17012542798525856, binarize=0.0, class_prior=None,fit_prior=True)
clf_description = BernoulliNB(alpha=0.00062355073412739121, binarize=0.0, class_prior=None, fit_prior=True)
clf_prob = LogisticRegression(C=1, class_weight='balanced', dual=False, fit_intercept=True, intercept_scaling=0.2, 
                              max_iter=100, multi_class='ovr', n_jobs=1, penalty='l2', random_state=None, solver='liblinear', 
                              tol=0.0001, verbose=0, warm_start=False)

clf_text.fit(trn_text_bow,trn_text_classes_bow) 
clf_description.fit(trn_description_bow,trn_description_classes_bow)
trn_prob,trn_prob_class=prepare_combined_model(clf_text,clf_description,vectorizer_text,vectorizer_description,test_set)
clf_prob.fit(trn_prob, trn_prob_class)


# ###################### Add genders for each user #######################
print 'Predicting...'
user = defaultdict(list)
image_url = {}
for id in database:
    document = database[str(id)]
    if document['gender'] == None and len(user[document['user']['id']]) < 5:
        if document['user']['profile_image_url'] != None and document['user']['default_profile_image'] == False:

            profile_image = re.sub('_normal', '', document['user']['profile_image_url'])
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

        if document['text'] != None:
            prob_text = predict_bow(document['text'], vectorizer_text, clf_text)
        else:
            prob_text = 0.5
        if document['user']['description'] != None:
            prob_description = predict_bow(document['user']['description'], vectorizer_description, clf_description)
        else:
            prob_description = 0.5

        gender = clf_prob.predict([[prob_text,prob_description,face_results]])[0]

        document['gender'] = gender
        user[document['user']['id']].append(gender)
        database.save(document)
        print str(id), 'completed as', gender
    elif(document['gender'] == None and len(user[document['user']['id']]) >= 5):
        male_count = 0
        female_count = 0
        for each in user[document['user']['id']]:
            if each == 'male':
                male_count += 1
            else:
                female_count += 1
        if male_count > female_count:
            document['gender'] = 'male'
        else:
            document['gender'] = 'female'
        database.save(document)
        print str(id), 'completed as', gender


####################### TEST ##########################
# f = open(test_set, 'r').read()
# rows = f.split('\n')
# pairs = []
# testset = []
# classes = []
# predicts = []
# genders = []
# count_correct = 0
# count_text = 0
# count_description = 0
# count_image = 0
# count = 0
# count_male = 0
# count_female = 0
# tp = []

# for row in rows:
#     pairs.append(row.split('\t'))
# for pair in pairs:
#     if len(pair) == 6:
#         testset.append(pair)    

# for each in testset:
# #     if len(each[1]) >= 25:
#     prob_text = predict_bow(each[1].decode('utf-8'), get_bigrams_BOW, vectorizer_text, clf_text)
#     prob_description = predict_bow(each[2].decode('utf-8'), get_bigrams_BOW, vectorizer_description, clf_description)
#     prob_image = float(each[4]) - (float(each[4]) - 0.5)/2
#     prob = clf_prob.predict_proba([[prob_text,prob_description, prob_image]])[0][0]
#     classes.append(each[0])
#     predicts.append(prob)
#     genders.append(get_gender(prob))

#     if each[0] == 'male':
#         tp.append(0)
#     else:
#         tp.append(1)

#     if get_gender(prob) == each[0] and each[0] == 'male':
#         count_male += 1
#         count_correct += 1
#     elif get_gender(prob) == each[0] and each[0] == 'female':
#         count_female += 1
#         count_correct += 1

#     if get_gender(prob_text) == each[0]:
#         count_text += 1

#     if get_gender(prob_description) == each[0]:
#         count_description += 1
    
#     if get_gender(prob_image) == each[0]:
#         count_image += 1
        
#     count += 1

# print 'Test Set Accuracy:'
# print 'Male:', count_male, 'Female:', count_female
# print 'Text:', count_text / float(count)
# print 'Description:', count_description / float(count)
# print 'Image:', count_image / float(count)
# print 'Total:', count_correct / float(count)

# print classification_report(classes,genders)
# false_positive_rate, true_positive_rate, thresholds = roc_curve(tp,predicts)
# print false_positive_rate, true_positive_rate, thresholds
# roc_auc = auc(false_positive_rate, true_positive_rate)
# print 'AUC:', roc_auc
# print 'Log-loss:', log_loss(tp,predicts)

#Draw the ROC Curve
# plt.title('Receiver Operating Characteristic')
# plt.plot(false_positive_rate, true_positive_rate, 'b', label='AUC = %0.3f'% roc_auc)
# plt.legend(loc='lower right')
# plt.plot([0,1],[0,1],'k--')
# plt.xlim([0.0,1.0])
# plt.ylim([0.0,1.0])
# plt.ylabel('True Positive Rate')
# plt.xlabel('False Positive Rate')
# plt.show()

print datetime.now() - startTime


# In[ ]:




# In[ ]:




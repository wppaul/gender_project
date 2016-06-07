# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This file contain methods which is loading the data from CouchDB as a csv file for linear regression analysis
# encoding=utf8  

import sys 
import json
import couchdb
import csv

reload(sys)  
sys.setdefaultencoding('utf8')

couch = couchdb.Server('http://115.146.89.191:5984')

database = couch['absdata']

csv_file = open('suburb.csv','ab')
writer = csv.writer(csv_file)
writer.writerow(["postcode","male","female","male_over_1","female_over_1","male_over_2","female_over_2","male_over_3","female_over_3"])

for id in database:
    tweet = database[str(id)]
    postcode = str(id)
    if tweet['properties'].has_key('female_over_3') and tweet['properties'].has_key('male_over_3'):
        male = tweet['properties']['male']
        female = tweet['properties']['female']
        male_over_1 = tweet['properties']['male_over_1']
        female_over_1 = tweet['properties']['female_over_1']
        male_over_2 = tweet['properties']['male_over_2']
        female_over_2 = tweet['properties']['female_over_2']
        male_over_3 = tweet['properties']['male_over_3']
        female_over_3 = tweet['properties']['female_over_3']

        output_row = postcode + ","+ str(male) + "," + str(female) + "," + str(male_over_1)+ "," + str(female_over_1)+ ","  + str(male_over_2)+ "," + str(female_over_2)+ "," + str(male_over_3)+ "," + str(female_over_3)+ "\n"
        csv_file.write(bytes(output_row))
        print(output_row)
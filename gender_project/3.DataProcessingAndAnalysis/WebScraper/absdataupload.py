# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This file contain methods which push the data from GreatMelbourneCensusData.csv to couchdb for visualization purpose

import csv
import couchdb

# create and connect to database
couch = couchdb.Server('http://115.146.89.191:5984/')
data_base_name = 'absdata'
try:
    data_base = couch.create(data_base_name)
except couchdb.http.PreconditionFailed as e:
    data_base = couch[data_base_name]

with open('CompleteGreatMelbourneCensusData.csv','r') as f:
    reader = csv.reader(f)
    next(reader, None) # skip the headers
    # read each attributes from csv file and upload to database
    for eachline in reader:
        newdocument = data_base[eachline[0]]
        newdocument['properties']['suburb'] = eachline[1]
        newdocument['properties']['people'] = eachline[2]
        newdocument['properties']['male'] = eachline[3] 
        newdocument['properties']['female'] = eachline[4]
        newdocument['properties']['malepercentage'] = eachline[5]
        newdocument['properties']['femalepercentage'] = eachline[6]
        newdocument['properties']['medianage'] = eachline[7]
        newdocument['properties']['families'] = eachline[8]
        newdocument['properties']['averagechildren'] = eachline[9]
        newdocument['properties']['allprivatedwellings'] = eachline[10]
        newdocument['properties']['avgpeopleperhousehold'] = eachline[11]
        newdocument['properties']['medianweeklyhouseholdincome'] = eachline[12]
        newdocument['properties']['medianmortgagerepayments'] = eachline[13]
        newdocument['properties']['medianweeklyrent'] = eachline[14]
        newdocument['properties']['avgvehiclesperdwelling'] = eachline[15]
        newdocument['properties']['unemploymentrate'] = eachline[16]
        data_base.save(newdocument)
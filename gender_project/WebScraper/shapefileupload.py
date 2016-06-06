# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This file contain methods which push the data from GreatMelbourneCensusData.csv to couchdb for visualization purpose

import json
import couchdb

# create and connect to database
couch = couchdb.Server('http://115.146.89.191:5984/')
data_base_name = 'absdata'
try:
    data_base = couch.create(data_base_name)
except couchdb.http.PreconditionFailed as e:
    data_base = couch[data_base_name]

with open("greaterMelbourne.json") as f:
    shape_data = json.load(f)['features']
    for geodata in shape_data:
        if('postcode' in geodata['properties']):
            geodata['_id'] = geodata['properties']['postcode']
            # transforming the geodata to match the requirement of the google map
            transformed_coordinates = []
            for eachelement in geodata['geometry']['coordinates']:
                eachelement[0] = eachelement[0] - 180
                eachelement[1] = -1*eachelement[1] + 180
                transformed_coordinates.append(eachelement)
            geodata['geometry']['coordinates'] = transformed_coordinates
            if ('name' in geodata['properties']):
                del geodata['properties']['name']
            del geodata['properties']['pfi']
            del geodata['properties']['yr2011_12']
            try:
                data_base.save(geodata)
            except Exception as e:
                print (geodata["_id"], e)
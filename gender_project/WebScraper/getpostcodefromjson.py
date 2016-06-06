# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This file contain methods which extract postcode and suburb name from greaterMelbourne.json in order to performing
# web scraping on Australian Bureau of Statistics website
import json
import csv

temp = {}
csv_file = open('suburbandpostcode.csv','ab')
writer = csv.writer(csv_file)
writer.writerow(["Postcode","Suburb"])
with open("greaterMelbourne.json") as json_file:
    json_data = json.load(json_file)['features']
    for data in json_data:
        if('postcode' in data['properties']):
            if ('name' in data['properties']):
                temp[data['properties']['postcode']] = data['properties']['name'].replace("?", " ")\
                .replace("-", " ").replace("+", " ")
            else:
                temp[data['properties']['postcode']] = 'N/A'
for k,v in sorted(temp.iteritems()):
    # print k,v
    output = k +"," +v +"\n"
    # print output
    csv_file.write(bytes(output))
    # postcode.append(k)
    # suburb.append(v)
# print postcode
# print suburb
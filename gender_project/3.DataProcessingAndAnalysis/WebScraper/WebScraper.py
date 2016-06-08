# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
# This file contain methods which systemtically scraping target data by performing regular expression search
# from Australian Bureau of Statistics website, all the data will be saved to a csv file named GreatMelbourneCensusData.csv

import urllib2
import re
import csv

postcode_list = []
profile_pattern = re.compile(r'<td class="summaryData">(.+)</td>')
unemploy_pattern = re.compile(r"and\s(.+)\%\swere\sunemployed")

with open('postcode.txt','r') as f:
    for line in f:
        postcode_list.append(line.strip())
csv_file = open('GreatMelbourneCensusData.csv','ab')
writer = csv.writer(csv_file)
writer.writerow(["Postcode","People", "Male", "Female","MalePercentage","FemalePercentage","MedianAge","Families","AverageChildren","AllPrivateDwellings","AvgPeopleperHousehold","MedianWeeklyHouseholdIncome","MedianMortgageRepayments","MedianWeeklyRent","AvgVehiclesperDwelling","UnemploymentRate"])
for postcode in  postcode_list:
    url_link = "http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/POA" + postcode + "?opendocument&navpos=220"
    url = urllib2.urlopen(url_link)
    content = url.read()
    profile = profile_pattern.findall(content)
    Totalpeople = ''
    Male = ''
    Female = ''
# Index start from 0 to 11
# Total People=>0,Male=>1,Female=>2, Median age=>3, Families=> 4, 
# Average children per family=> 5
# All private dwellings=>6,Average people per household =>7,
# Median weekly household income =>8,Median monthly mortgage repayments =>9
# Median weekly rent => 10, Average motor vehicles per dwelling=>11
    try:
        Totalpeople = profile[0].replace(",","")
    except IndexError:
        Totalpeople = "null"
    try:
        Male = profile[1].replace(",","")
    except IndexError:
        Male = "null"
    try:
        Female = profile[2].replace(",","")
    except IndexError:
        Female = "null"
    try:
        Median_age = profile[3]
    except IndexError:
        Median_age = "null"
    try:
        Families = profile[4].replace(",","").replace(",","")
    except IndexError:
        Families = "null"
    try:
        Average_children = profile[5].replace(",","")
    except IndexError:
        Average_children = "null"
    try:
        private_dwellings = profile[6].replace(",","")
    except IndexError:
        private_dwellings = "null"
    try:
        people_per_household = profile[7].replace(",","")
    except IndexError:
        people_per_household = "null"
    try:
        weekly_household_income = profile[8].replace(",","").replace("$","")
        # print weekly_household_income
    except IndexError:
        weekly_household_income = "null"
    try:
        mortgage_repayments = profile[9].replace(",","").replace("$","")
        # print mortgage_repayments
    except IndexError:
        mortgage_repayments = "null"
    try:
        weekly_rent = profile[10].replace(",","").replace("$","")
        # print weekly_rent
    except IndexError:
        weekly_rent = "null"
    try:
        vehicles_per_dwelling = profile[11].replace(",","")
    except IndexError:
        vehicles_per_dwelling = "null"
    try:
        unemploy_rate = unemploy_pattern.findall(content)[0].replace(",","")
    except IndexError:
        unemploy_rate  = "null"
    if Totalpeople!='null' and Male !='null' and Female !='null':
        male = float(profile[1].replace(',',''))
        female = float(profile[2].replace(',',''))
        total = float(profile[0].replace(',',''))
        male_per = str(round(male/total*100, 1))
        female_per = str(round(female/total*100, 1))
    else:
        male_per = 'null'
        female_per = 'null'
    
    output = postcode+","+Totalpeople+","+Male+","+Female+","+ male_per+ ","+ female_per+\
             ","+Median_age+","+Families+","+Average_children+","+private_dwellings+","+\
             people_per_household+","+ weekly_household_income+","+ mortgage_repayments+","+\
             weekly_rent+","+ vehicles_per_dwelling+","+ unemploy_rate +"\n"
    # print output
    csv_file.write(bytes(output))
Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
==========================================================================================================

        Author :  PENG WANG  Student Number : 680868             
        Author :  MINGYU GAO Student Number : 692634
        Supervisor : Prof. Richard Sinnott
        Subject: COMP90055 COMPUTING PROJECT

*************** Demo URL *************************

Website: http://115.146.89.193:3009/
YouTube: https://youtu.be/SSFw2UIRwj8
Souce Codes: https://github.com/wppaul/gender_project

*************** System requirement ***************
Ubuntu: version":"15.10"

Couchdb:"version":"1.6.0"

Python: "version": "2.7.10" with:
    - pip (8.1.1)
    - nltk (3.2)
    - Textblob(0.11.1)
    - CouchDB (0.8)
    - tweepy (3.5.0)
    - googlemaps (2.4.3)
    - genderizer (0.1.2.3)
    - pymongo (3.2.2)
    - python-memcached (1.57)
    - naiveBayesClassifier (0.1.3)
    - scikit-learn (0.17.1)
    - numpy (1.11.0)
    - requests (2.9.1)

Rails "version": "4.1.10" with:
    - ruby-dev
    - zlib1g-dev
    - liblzma-dev
    - ruby
    - ruby-railties
    - git
    - bundler
    - libsqlite3-dev

*************** File Directory Listing ***********

1. SystemInstallation
2. TweetsHarvesters
3. DataProcessingAndAnalysis
4. MVCWebApplication

*************** File Directory Details ***********

1. SystemInstallation : This File Contains System Development Automation Tools Boto and Ansible

##Boto 
This folder contains a python file which is used for launching instances and attaching volumes

##Ansible
This folder contains yml files and roles which is used for automatically deploying the application as well as perform any necessary configuration.

yml files:
--site.yml         # master playbook
--startboto.yml    # playbook for starting boto
--allservers.yml   # playbook for all servers
--webservers.yml   # playbook for web servers

roles:
--updatecache             #update the cache in ubuntu
--sharedsoftware          #install the share package in ubuntu
--machinelearningpackage  #install the machine learning package in ubuntu
--mountvolume             #mount volumes
--installcouchdb          #install couchdb and edit configurations
--pushfiles               #push files to servers
--startharvester          #start tweets harvester on servers
--rails                   #install web related packages 
--startwebserver          #start web server
--startboto               #run boto

Please refer to README.md to run the scripts in System Installation

2.TweetsHarvesters : This File Contains Tweets Harvesters Scripts

3.DataProcessingAndAnalysis : This File Contains Data Processing tools and Machine Learning Development Proecess

4.MVCWebApplication : This File Constains Web Application Files developed by Ruby on Rails

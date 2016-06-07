import requests
import time
import json
import csv
try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json

s = requests.Session()
url_list =[]

with open('final_male','r') as f:
    for line in f.readlines():
        url_list.append(line.strip('\n'))

def get_res(url):
    params = dict()
    params['apikey'] = '9631426b3923f8d14af627189c25df7733f3c3a2'
    params['outputMode'] = 'json'
    endpoint = '/url/URLGetRankedImageFaceTags'
    BASE_URL = 'http://access.alchemyapi.com/calls'
    params['url'] = url
    post_url = ""
    try:
        post_url = BASE_URL + endpoint + \
            '?' + urlencode(params).encode('utf-8')
    except TypeError:
        post_url = BASE_URL + endpoint + '?' + urlencode(params)

    try:
        results = s.post(url=post_url)
        if not results.json()["imageFaces"]:
            return "NoFace"
        else:
            temp = results.json()["imageFaces"][0]
            # print temp
            return temp["gender"]["gender"] + ',' + temp["gender"]["score"] + ',' + temp["age"]["ageRange"] + ',' + temp["age"]["score"]
    except Exception as e:
        print e
        return "error"

if __name__ == '__main__':
    csv_file = open('ibm_male.csv','ab')
    writer = csv.writer(csv_file)
    writer.writerow(["ID","URL","GENDER","CONFIDENCE","AGE","CONFIDENCE"])
    count = 1
    total_count = 1
    for url in url_list:
        if count > 250:
            time.sleep(60*60)
            count = 1
        results = get_res(url)
        count +=1
        if results == 'NoFace':
           output = str(total_count) + ','+ url + ',' + str(results) + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        elif results == 'error':
           output = str(total_count) + ','+ url + ',' + str(results) + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        else:
           output = str(total_count) + ','+ url + ',' + results + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        print total_count
        time.sleep(2)

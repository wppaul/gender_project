# encoding=utf8  
import sys 
import json
import couchdb
import csv
from facepp import API
from facepp import File
import time

reload(sys)  
sys.setdefaultencoding('utf8')


SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = '98ba2c74c58ca1e2b9ccfafb047669a5'
API_SECRET = 'L98vUONg9V3Sd9CIwExc-kOHG_hk6Nup'
api = API(API_KEY,API_SECRET,SERVER)

url_list = []

def get_face(newurl):
    try:
        face = api.detection.detect(url = newurl, mode='oneface')
        if not face['face']:
            return "NoFace"
        elif len(face['face']) > 1:
            return "MultipleFaces"
        else:
            return [face['face'][0]['attribute']['gender']['value'],face['face'][0]['attribute']['gender']['confidence']]
    except Exception as e:
        pass
        return "error"

if __name__ == '__main__':
    count = 1 
    gender = "Male"

    with open('final_male.txt','r') as f:
        for line in f.readlines():
            url_list.append(line.strip('\n'))

    csv_file = open('face_male.csv','ab')
    writer = csv.writer(csv_file)
    writer.writerow(["COUNT","URL","FACEGENDER","CONFIDENCE","REALGENDER","SAME"])
    
    for i in url_list:
        try:
            results = get_face(i)
        except Exception as e:
            print e
            time.sleep(10)
            results = get_face(i)
        same = "False"     
        if results[0] == gender:
            same = "True"
        output = str(count)+ ','+ str(i)+',' + results[0] +','+str(results[1])+','+ gender + ',' +same + "\n"
        csv_file.write(bytes(output))
        print count
        count += 1
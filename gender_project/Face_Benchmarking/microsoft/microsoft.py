import httplib, urllib, base64
import json
import time
import csv

url_list = []

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = 'b7b49c5e74344630ab9c8fc231e9bf1a'
headers['Content-type'] = 'application/json'

with open('final_male.txt','r') as f:
    for line in f.readlines():
        url_list.append(line.strip('\n'))

def detect_face(body):
    params = urllib.urlencode({
        # Request parameters
        'returnFaceId':'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile'
    })
    try:
       conn = httplib.HTTPSConnection('api.projectoxford.ai')
       conn.request("POST", "/face/v1.0/detect?%s" % params, '{\'url\' : \'%s\'}'%body , headers)
       response = conn.getresponse()
       # print("Send request")
       temp = response.read()
       data =json.loads(temp)
       return data[0]['faceAttributes']
       # print(data[0]['faceAttributes'])
       conn.close()
    except IndexError:
       return 'NoFace'
    except KeyError:
       return 'error'
    except Exception as e:
       print("[Errno {0}] {1}".format(e.errno, e.strerror))
       return 'error'

if __name__ == '__main__':
    csv_file = open('mic_male.csv','ab')
    writer = csv.writer(csv_file)
    writer.writerow(["ID","URL","GENDER","AGE","SMILE","REALGENDER","SAME"])

    total_count = 1
    gender = "male"
    for url in url_list:
      same = "False"
      results = detect_face(url)
      if results == 'NoFace':
         output = str(total_count) + ','+ url + ',' + str(results) + ','+ same +'\n'
         csv_file.write(bytes(output))
         total_count+=1
      elif results == 'error':
         output = str(total_count) + ','+ url + ',' + str(results) + ','+ same +'\n'
         csv_file.write(bytes(output))
         print total_count
      else:
         if results['gender'] == gender:
              same='True'
         if 'smile' not in results:
              results['smile'] = "No"
         if 'age' not in results:
              results['age'] = "No"
         output = str(total_count) + ','+ url + ',' + str(results['gender']) + ',' + str(results['age']) + ','+ str(results['smile'])+ ','+gender+','+ same +'\n'
         csv_file.write(bytes(output))
         print total_count
         total_count+=1
      time.sleep(5)
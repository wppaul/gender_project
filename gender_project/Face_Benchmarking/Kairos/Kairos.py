from urllib2 import Request, urlopen
import json
import csv
import time

url_list =[]
with open('final_male.txt','r') as f:
    for line in f.readlines():
        url_list.append(line.strip('\n'))

def get_gender(url):
  values = """
    {
      "image": "%s",
      "selector": "FULL"
    }
  """%url

  headers = {
    'Content-Type': 'application/json',
    'app_id': 'd354cefb',
    'app_key': '78b315e8359fc5580e2895a473bf6f95'
  }
  request = Request('https://api.kairos.com/detect', data=values, headers=headers)

  try:
     data = json.load(urlopen(request))
     if data.has_key('Errors'):
        return "NoFace"
     else:
      # print data
      # print data['images'][0]['faces'][0]['attributes']['gender']['type']
      # print data['images'][0]['faces'][0]['attributes']['gender']['confidence']
         return data['images'][0]['faces'][0]['attributes']['gender']['type'] + ',' + data['images'][0]['faces'][0]['attributes']['gender']['confidence']
  except KeyError:
    pass
    return "NoFace"

if __name__ == '__main__':
    csv_file = open('Kairos_male','ab')
    writer = csv.writer(csv_file)
    writer.writerow(["ID","URL","GENDER","CONFIDENCE"])

    total_count = 1
    for url in url_list:
        results = get_gender(url)
        if results == 'NoFace':
           output = str(total_count) + ','+ url + ',' + str(results) + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        elif results == 'error':
           output = str(total_count) + ','+ url + ',' + str(results) + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        else:
           output = str(total_count) + ','+ url + ',' + str(results) + '\n'
           csv_file.write(bytes(output))
           total_count+=1
        time.sleep(6)



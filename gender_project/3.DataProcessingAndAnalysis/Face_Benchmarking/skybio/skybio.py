# Copyright (c) 2010, 2011, Tomaž Muraus
# All rights reserved.

from face_client import FaceClient
import json
import csv
import time

client = FaceClient('88c2f662703642d99d67bce4400bbebf', 'd5d89a3b8a8c42dfafb94a19728a183d')

# print response['photos'][0]['tags'][0]['attributes']['gender']['value']
# print response['photos'][0]['tags'][0]['attributes']['gender']['confidence']

url_list =[]

with open('final_male.txt','r') as f:
    for line in f.readlines():
        url_list.append(line.strip('\n'))

if __name__ == '__main__':

    csv_file = open('sky_male.csv','ab')
    writer = csv.writer(csv_file)
    writer.writerow(["ID","URL","GENDER","CONFIDENCE"])

    total_count = 1
    for url in url_list:
        try:
            response = client.faces_detect(url)
            # print response
            if response['photos'][0]['tags'] == []:
               temp ='NoFace'
               output = str(total_count) + ','+ url + ',' + str(temp) + '\n'
               csv_file.write(bytes(output))
               total_count+=1
               pass
            else:
                gender = response['photos'][0]['tags'][0]['attributes']['gender']['value']
                confidence =response['photos'][0]['tags'][0]['attributes']['gender']['confidence']
                output = str(total_count) + ','+ url + ',' + str(gender) + ','+ str(confidence) + '\n'
                csv_file.write(bytes(output))
                total_count+=1
            print total_count
            if response['usage']['remaining'] == 1:
                print "i am sleeping"
                time.sleep(60*60)
        except Exception as e:
            print e
            output = str(total_count) + ','+ url + ',' + str(e) + '\n'
            csv_file.write(bytes(output))
            total_count+=1
        time.sleep(2)

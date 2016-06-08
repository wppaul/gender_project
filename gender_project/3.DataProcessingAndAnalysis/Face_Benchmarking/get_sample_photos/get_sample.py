# encoding=utf8  
import sys 
import couchdb
import csv
import random

reload(sys)  
sys.setdefaultencoding('utf8')

couch = couchdb.Server('http://115.146.89.191:5984')

try:
    data_base = couch.create('all_clubs')
except couchdb.http.PreconditionFailed as e:
    data_base = couch['all_clubs']

countlist = []
results = data_base.view('club/checkfemale')

for row in data_base.view('club/checkfemale',group_level = 1):
    countlist.append(str(row.key))

print len(countlist)

if __name__ == '__main__':

    numger_list = [1,2,3,4,5,6]
    counter = 1
    with open('female.txt', 'a+') as f:
        for url in countlist:
            if counter > 2000:
                break
            number = random.choice(numger_list)
            if number%2 == 0:
                # with open('female.txt', 'a+') as f:
                f.write(str(url) + '\n')
                print counter
                counter += 1
            else:
                print "skip this one"
                pass
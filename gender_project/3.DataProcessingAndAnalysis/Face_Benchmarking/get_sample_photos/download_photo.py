import urllib


url_list =[]
if __name__ == '__main__':

    with open('final_female.txt','r') as f:
        for line in f.readlines():
            url_list.append(line.strip('\n'))
            
    count = 1

    for i in url_list:
        try:
            urllib.urlretrieve(i, "%d.jpg"%count)
            print count
            count += 1
        except Exception as e:
            count += 1
            print e
            pass
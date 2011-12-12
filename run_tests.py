import urllib, json

url = 'http://172.16.162.11:9003/mapreduce/test_job?request='
jobs = {'test_wiki_read.py' : 10}

urllib.urlopen(url+jobs).read()

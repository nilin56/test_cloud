case = ['test_wiki_read.py', 'test_wiki_search.py', 'test_wiki_write']
num = [30, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720]
base_url = 'http://192.168.0.126:9002/mapreduce/test_job?request='

import json
import urllib
cube = {}
for c in case:
    print c
    for n in num:
        print n,
        s = json.dumps({c :n}) 
        r = urllib.urlopen(base_url + s ).read()
        r = json.loads(r)
        print r['total_pass_num']*1.0/n, 
        print r['request_num']*1.0/(float(r['max']['time'])-float(r['min']['time'])),
        print r['request_total_time']/r['request_num']

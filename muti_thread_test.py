import threading
import os
import json
import time


def exe_script(script_name, result_list):
    command = 'python %s'%script_name
    dict_str = os.popen(command).read()
    result_list.append(json.loads(dict_str))

def run(script_name, n):
    result_list = []
    threads = []
    for i in range(n):
        t = threading.Thread(target=exe_script, args=(script_name, result_list))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return result_list

def reduce(dicts):
    result = {}
    for d in dicts:
        for k, v in d.iteritems():
            if k in result:
                result[k] += v
            else :
                result[k] = v
    return result

def main(script_name, n):
    s= time.time()
    dicts = run(script_name, n)
    last = time.time()-s
    result = reduce(dicts)
    result['last'] = last
    return result

if __name__ == '__main__':
    from time import sleep
    for n in (1, 2, 5, 10, 15, 20, 25 ,30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160,180, 200):
        print n,
        #for script in ['test_wiki_write.py']:
        for script in ['test_wiki_read.py', 'test_wiki_search.py']:
            result = main(script, n)

            del(result['results'])
            print '%s'%(n*1.0/result['last']),
            sleep(10)
        print ''

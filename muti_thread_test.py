import threading
import os
import json
import time


def exe_script(script_name, result_list):
    executor = {
        'py' : 'python',
        'js' : 'javascript'
    }
    try:
        script_type = script_name.split('.')[-1] 
        command = '%s %s'%(executor[script_type], script_name)
        dict_str = os.popen(command).read()
        result_list.append(json.loads(dict_str))
    except:
        result_list.append({'script_execution_error_num': 1 })

def run(script_name, n):
    result_list = []
    threads = []
    for i in range(n):
        t = threading.Thread(target=exe_script, args=(script_name,result_list))
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

def exe_script_n_times(script_name, n, result_list):
    #in case float type on script_time
    n = int(n)
    dicts = run(script_name, n)
    result = reduce(dicts)
    result_list.append(result)

def main(task_dict):
    result_list = []
    threads = []
    for script_name, n in task_dict.items():
        t = threading.Thread(target=exe_script_n_times, args=(script_name, n, result_list))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return reduce(result_list)

if __name__ == '__main__':
    print main({'test_wiki_read.py':2, 'test_wiki_search.py':3})

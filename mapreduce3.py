import web
import json
#request url is : http://0.0.0.0:9003/mapreduce/capacity?request={%22mem%22:%201000,%20%22latency%22:%20100,%20%22cpu%22:%200.01}
#CHILDREN = {9000:['http://0.0.0.0:9001'],9001:['http://0.0.0.0:9002','http://0.0.0.0:9003'],9002:[],9003:[],9004:[]}
from node_map import NODE_MAP as CHILDREN
urls = (
    '/mapreduce/(.*)','mapreduce',
    '/port','port',
    '/children','children',
    )
app = web.application(urls, globals())

class port:
    def GET(self,task=None):
        return str(web.ctx).replace(',',',\n').replace('{','\n\n\n{').replace('}','}\n\n\n')

class children:
    def GET(self,task=None):
        port = web.ctx['env']['HTTP_HOST']
        print (CHILDREN[port])
        return (CHILDREN[port]).__str__().replace(',', ',\n')


class mapreduce:
    def GET(self,taskName=None):
        self.para = web.input()

        tasks = json.loads(web.input().request)

        if CHILDREN[self.my_port()]:
            return self.mapreduce(taskName, tasks)
        else :
            return self.worker(taskName, tasks)
       

    def mapreduce(self,taskName, tasks):
        return self.reducer(self.mapper(taskName, tasks))
            
    def mapper(self,taskName, tasks):
        import threading
        print 'map to children'

        resultList = []   
        threads = []
        
        nloops = range(len(CHILDREN[self.my_port()]))

        for script, num in tasks.items():
            tasks[script] = (num*1.0/len(nloops))

        for i in nloops:
            t = threading.Thread(target = call, args=(CHILDREN[self.my_port()][i], resultList, taskName, tasks))
            threads.append(t)
        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()
        return resultList   
            
    def reducer(self,resultList):
        result = {}
        for i in resultList:
            for k, v in i.items():
                if k in result.keys():
                    if k not in ['max', 'min']:
                        result[k] += v
                    else:
                        methods = {'max':max, 'min':min}
                        for kk, vv in v.items():
                            result[k][kk] = methods[k](str(vv), result[k].get(kk, '0'))
                else:
                    result[k] = v
        print 'finish reduce results'
        return json.dumps(result)
     
    def worker(self, taskName, tasks):
        print 'work on %s'%taskName
        if taskName == 'capacity':
            return capacity_worker(tasks)
        elif taskName == 'test_job':
            return test_worker(tasks)

    def my_port(self):
        return str(web.ctx['env']['HTTP_HOST'])

def test_worker(tasks):
    #tasks is a dict as{'a.py':2, 'b.py':3}
    from muti_thread_test import main as muti_test
    return json.dumps(muti_test(tasks))

def capacity_worker(tasks):
    request = tasks            
    MEM_PER = float(request['mem'])   
    CPU_PER = float(request['cpu'])
    LATENCY = float(request['latency'])

    import os
    cpuload = os.popen('uptime').read().split(' ')[-1]
    memfree = os.popen('cat /proc/meminfo | grep MemFree').read().split(' ')[-2]

    cpucount = (1-float(cpuload))/float(CPU_PER)
    memcount = float(memfree)/float(MEM_PER)
    l = latency(5)

    print 'cpucount', cpucount
    print 'memcount', memcount
    print 'latency',l
    
    late = l > LATENCY
    print str(late)
 
    if late :
        netcount = 0
    else:
        netcount = 10000000000
    count = min(cpucount, memcount, netcount)
    return json.dumps({'machine_count' : 1, 'capacity' : int(count)})

def call(child, resultList, taskName, tasks):
    query = '?request=' + json.dumps(tasks)
    url = child+'/mapreduce/'+ taskName +query
    print 'call: %s'%url
    import urllib2
    import urllib
    try:
        result = json.loads(urllib.urlopen(url).read())
    except:
        result = {'fail_node': [url]}
    print 'child(%s) get result'%child
    resultList.append(result)
  
def latency(minute=None):
    import os
    re=0.0
    if minute:            
        out = os.popen("tail -n" + str(int(12)*int(minute)) + " ping.out|grep time=|cut -d '=' -f 4").read().split(' ms\n')
        out = out[0:-1]            
    else:
        out = os.popen("cat ping.out|grep time=|cut -d '=' -f 4").read().split(' ms\n')
        out = out[0:-1]                     
       
    for l in out:
        re += float(l)
    return re/len(out)

def update_ping():
    import os
    os.popen("rm ping.out")
    os.popen("nohup ping www.baidu.com > ping.out &")

if __name__ == '__main__':
    update_ping()
    app.run()
            

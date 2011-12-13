import urllib, urllib2

real_urlopen = urllib.urlopen
def _urlopen(a):
    import os
    import time
    import json
    pid = os.getpid()
    fname = 'pid_%s_delay'%pid

    t_start = time.time()
    r = real_urlopen(a)
    t_end = time.time()
    
    try:
        f = open(fname, 'r')
        delays = json.loads(f.read())
    except IOError:
        delays = []
    
    delays.append([t_end - t_start, t_start])
    f = open(fname, 'w')
    f.write(json.dumps(delays))

    return r
urllib.urlopen = _urlopen

real_urlopen2 = urllib2.urlopen
def _urlopen2(a):
    import os
    import time
    import json
    pid = os.getpid()
    fname = 'pid_%s_delay'%pid

    t_start = time.time()
    r = real_urlopen2(a)
    t_end = time.time()
    
    try:
        f = open(fname, 'r')
        delays = json.loads(f.read())
    except IOError:
        delays = []
    
    delays.append([t_end - t_start, t_start])
    f = open(fname, 'w')
    f.write(json.dumps(delays))

    return r
urllib2.urlopen = _urlopen2


def dictsonize(func):
    import json
    import time
    def _(*a, **kw):
        start = time.time()

        r =func(*a, **kw)

        end = time.time()

        try:
            import os
            pid = os.getpid()
            fname = 'pid_%s_delay'%pid
            f = open(fname, 'r')
            delays = json.loads(f.read())
            os.remove(fname)
        except IOError:
            delays = []

        ret = {'time':0, 'request_num' : len(delays), 'request_total_time' : sum( [delay for delay, start_time in delays])}
        ret['%s_%s_num'%(func.__name__, r)] = 1
        ret['%s_%s_num'%('total', r)] = 1
        ret['time'] = end - start
        try:
            ret['max']={}
            ret['max']['time'] = delays[-1][1]
            ret['max']['test_time'] = end -start
            ret['max']['delay'] = max(delays)[0]
            ret['min']={}
            ret['min']['time'] = delays[0][1]
            ret['min']['delay'] = min(delays)[0]
        except IndexError:
            pass

        '''
        ret.update({'results' : [{
                        'start':start, 
                        'end':end,
                        'result': r,
                        'time' : end - start,
                        'request_num' : len(delays),
                        'request_total_time' : sum([delay for delay, start_time in delays]),
                        'delays' : delays
                        }]
                    })
        '''
        return json.dumps(ret)
    return _

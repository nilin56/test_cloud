import urllib

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

        ret = {'fail_num': 0, 'pass_num': 0, 'error_num': 0, 'time':0, 'request_num' : len(delays), 'request_total_time' : sum( [delay for delay, start_time in delays])}
        ret['%s_num'%r] = 1
        ret['time'] = end - start

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
        return json.dumps(ret)
    return _

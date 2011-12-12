cmds = [
    'ps -ef|grep mapreduce|grep -v grep |cut -c 9-15|xargs kill -9',
    'nohup python mapreduce3.py 9003 &'
]

import os
tmp = ''
tmp += os.popen(cmds[0]).read()
tmp += 'done'
os.popen(cmds[1])
print tmp
    

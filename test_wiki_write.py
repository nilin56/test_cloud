import urllib, urllib2, sys, re
url = "http://123.138.22.46/dokuwiki/doku.php"

import time
header = {
"Host": "123.138.22.46",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2",
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Referer": "http://123.138.22.46/dokuwiki/doku.php",
"Accept-Encoding": "gzip,deflate,sdch",
"Accept-Language": "zh-CN,zh;q=0.8",
"Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
"Cookie": "DokuWiki=icbeim0oi09bp4bi0jk1u8vje1"
}
import decorator
from decorator import dictsonize
@dictsonize
def test_w():
    try :
        title = 'trytrytrytry'+str(time.time())
    
        start = urllib.urlencode(
            [
                ('do', 'edit'),
                ('id', title),
                ('rev', ''),
            ]
        )


        req = urllib2.Request(url,start,header)
        fd = urllib2.urlopen(req)
        s = fd.read()

        changecheck = re.search(r"changecheck\" value=\"(\w+)",s).group(1)
        sectok = re.search(r"sectok\" value=\"(\w+)",s).group(1)

    #print changecheck,sectok

        confirm = urllib.urlencode(
            [
                ('changecheck',changecheck),
                ('do[save]', 'Save'),
                ('id', title),
                ('prefix', ''),
                ('rev', ''),
                ('sectok', sectok),
                ('summary', 'created'),
                ('wikitext', '123456712345671234567'),
            ]
        )


        req = urllib2.Request(url,confirm,header)
        fd = urllib2.urlopen(req)
        s = fd.read()
    except :
        print 'error'
        return 'error'
    if s.__contains__(title):
        return 'pass'
    else: 
        return 'fail'
def main():
    r = test_w()
    print r
    return r

if __name__ == '__main__':
    main()

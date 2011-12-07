import urllib
import decorator
from decorator import dictsonize

@dictsonize
def test_r():
    try:
        for i in range(10):
            url = 'http://123.138.22.46/dokuwiki/doku.php?id=sectok=733cbec27fa1fc3a8fb828a5d758c94d&id=nb&rev=&date=&prefix=&suffix=&changecheck=d41d8cd98f00b204e9800998ecf8427e&wikitext=1234567&do%5Bsave%5D=Save&summary=created'
            r = urllib.urlopen(url)
            r = urllib.urlopen(url)
            r = r.read()
            if not (r.__contains__('content') and len(r) > 200):
                return 'fail'
    except:
        return 'error'
    return 'pass'

def main():
    r = test_r()
    print r
    return r

if __name__ == '__main__':
    main()

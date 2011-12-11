import urllib
import decorator
from decorator import dictsonize

@dictsonize
def test_search():
    try:
        for i in range(10):
            url = 'http://123.138.22.46/dokuwiki/doku.php?do=search&id=content'
            r = urllib.urlopen(url)
            r = urllib.urlopen(url)
            r = r.read()
            if not (r.__contains__('content') and len(r) > 200):
                return 'fail'
    except:
        return 'error'
    return 'pass'

def main():
    r = test_search()
    print r
    return r

if __name__ == '__main__':
    main()

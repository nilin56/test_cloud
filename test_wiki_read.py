import urllib
import decorator
from decorator import dictsonize

@dictsonize
def test_r():
    try:
        url = 'http://123.138.22.46/dokuwiki/doku.php?do=search&id=content'
        r = urllib.urlopen(url)
        r = urllib.urlopen(url)
        r = r.read()
        if r.__contains__('content') and len(r) > 200:
            return 'pass'
        else :
            return 'fail'
    except:
        return 'error'

def main():
    r = test_r()
    print r

if __name__ == '__main__':
    main()

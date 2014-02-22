import urllib2
import re

class Relinker:
    __USERAGENT = "Mozilla/5.0 (Linux; Android 4.2.1; Nexus 7 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"

    def __init__(self):
        opener = urllib2.build_opener()
        # Use Firefox User-Agent
        opener.addheaders = [('User-Agent', self.__USERAGENT)]
        urllib2.install_opener(opener)

    def getURL(self, url):
        url = url + "&output=20"
        print "Relinker URL: %s" % url
        response = urllib2.urlopen(url)
        mediaUrl = response.read().strip()
        return mediaUrl

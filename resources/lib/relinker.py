import urllib2
import re

class Relinker:
    __USERAGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"

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

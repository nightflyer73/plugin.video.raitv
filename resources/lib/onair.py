import urllib2
import json
from StringIO import StringIO

class onAir:
    def getNowNext(self):
        url = "http://www.rai.it/dl/portale/html/palinsesti/static/palinsestoOraInOnda.html?output=json" 
        response = json.load(urllib2.urlopen(url))
        return response

    def getNowNextWR(self, stationId):
        # stationId = {fd4, fd5}
        # disabled for {wr6, wr7, wr8}
        url = "http://service.rai.it/xml2json.php?jsonp=?&xmlurl=http://frog.prodradio.rai.it/orainonda/%s/onair_%s.xml" % (stationId, stationId)
        text = urllib2.urlopen(url).read()
        text = text[2:-2]
        io = StringIO(text)
        response = json.load(io)
        return response["xml"]["radio"]

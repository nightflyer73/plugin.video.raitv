import sys
import urllib
import urllib2
import datetime
import json

class Replay:
    channels = {1: "RaiUno", 2: "RaiDue", 3: "RaiTre", 31: "RaiCinque"}
   
    def getProgrammes(self, channelId, epgDate):
        channel = self.channels[channelId]      
        url = "http://www.rai.tv/dl/portale/html/palinsesti/replaytv/static/%s_%s.html" % (channel, epgDate)
        response = json.load(urllib2.urlopen(url))
        return response[str(channelId)][epgDate.replace('_', '-')]


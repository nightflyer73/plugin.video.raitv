import sys
import urllib
import urllib2
import datetime
import json

class Replay:
    def getChannels(self):
        url = "http://www.rai.tv/dl/RaiTV/iphone/android/smartphone/advertising_config.html"
        response = json.load(urllib2.urlopen(url))
        channels = []
        for channel in response["Channels"]:
            if channel["hasReplay"] == "YES":
                channel["icon"] = channel["icon"].replace(".png", "-big.png")
                channels.append(channel)
        return channels
   
    def getProgrammes(self, channelId, channelName, epgDate):
        url = "http://www.rai.tv/dl/portale/html/palinsesti/replaytv/static/%s_%s.html" % (channelName, epgDate)
        print "Replay TV URL: %s" % url
        response = json.load(urllib2.urlopen(url))
        return response[str(channelId)][epgDate.replace('_', '-')]


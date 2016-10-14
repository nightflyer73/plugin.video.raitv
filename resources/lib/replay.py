import urllib2
import json

class Replay:
    def getProgrammes(self, channelName, epgDate):
        channelTag = channelName.replace(" ", "")
        url = "http://www.rai.it/dl/palinsesti/Page-e120a813-1b92-4057-a214-15943d95aa68-json.html?canale=%s&giorno=%s" % (channelTag, epgDate)
        response = json.load(urllib2.urlopen(url))
        return response[channelName][0]["palinsesto"][0]["programmi"]

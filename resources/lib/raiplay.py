# -*- coding: utf-8 -*-
import urllib2
import json
import re
import os
from tempfile import mkstemp
from HTMLParser import HTMLParser

class RaiPlay:
    # From http://www.raiplay.it/mobile/prod/config/RaiPlay_Config.json
    baseUrl = "http://www.rai.it/"
    channelsUrl = "http://www.rai.it/dl/RaiPlay/2016/PublishingBlock-9a2ff311-fcf0-4539-8f8f-c4fee2a71d58.html?json"
    localizeUrl = "http://mediapolisgs.rai.it/relinker/relinkerServlet.htm?cont=201342"
    menuUrl = "http://www.rai.it/dl/RaiPlay/2016/menu/PublishingBlock-20b274b1-23ae-414f-b3bf-4bdc13b86af2.html?homejson"
    palinsestoUrl = "http://www.rai.it/dl/palinsesti/Page-e120a813-1b92-4057-a214-15943d95aa68-json.html?canale=[nomeCanale]&giorno=[dd-mm-yyyy]"
    AzTvShowPath = "/dl/RaiTV/RaiPlayMobile/Prod/Config/programmiAZ-elenco.json"
    noThumbUrl = "http://www.rai.it/cropgd/256x144/dl/components/img/imgPlaceholder.png"
    
    def getCountry(self):
        response = urllib2.urlopen(self.localizeUrl).read()
        return response
        
    def getChannels(self):
        response = json.load(urllib2.urlopen(self.channelsUrl))
        return response["dirette"]
        
    def getProgrammes(self, channelName, epgDate):
        channelTag = channelName.replace(" ", "")
        url = self.palinsestoUrl
        url = url.replace("[nomeCanale]", channelTag)
        url = url.replace("[dd-mm-yyyy]", epgDate)
        response = json.load(urllib2.urlopen(url))
        return response[channelName][0]["palinsesto"][0]["programmi"]
        
    def getMainMenu(self):
        response = json.load(urllib2.urlopen(self.menuUrl))
        return response["menu"]

    # RaiPlay Genere Page
    # RaiPlay Tipologia Page
    def getCategory(self, pathId):
        url = self.getUrl(pathId)
        response = json.load(urllib2.urlopen(url))
        return response["blocchi"]
  
    # Raiplay Tipologia Item
    def getProgrammeList(self, pathId):
        url = self.getUrl(pathId)
        response = json.load(urllib2.urlopen(url))
        return response
    
    #  PLR programma Page
    def getProgramme(self, pathId):
        url = self.getUrl(pathId)
        response = json.load(urllib2.urlopen(url))
        return response
        
    def getContentSet(self, url):
        url = self.getUrl(url)
        response = json.load(urllib2.urlopen(url))
        return response["items"]
    
    def getVideoMetadata(self, pathId):
        url = self.getUrl(pathId)
        response = json.load(urllib2.urlopen(url))
        return response["video"]
    
    def getUrl(self, pathId):
        pathId = pathId.replace(" ", "%20")
        if pathId[0:2] == "//":
            url = "http:" + pathId
        elif pathId[0] == "/":
            url = self.baseUrl[:-1] + pathId
        else:
            url = pathId
        return url
        
    def getThumbnailUrl(self, pathId):
        if pathId == "":
            url = self.noThumbUrl
        else:
            url = self.getUrl(pathId)
            url = url.replace("[RESOLUTION]", "256x-")
        return url
    
    def fixSRT(self, url):
        # SubRip format
        # http://forum.doom9.org/showthread.php?p=470941#post470941
        hp = HTMLParser()
        output = ""

        data = urllib2.urlopen(url)
        for line in data.readlines():
            match = re.search(r"([:,\d]+)\s-->\s([:,\d]+)", line, re.DOTALL)
            if match is not None:
                # Fix timecode format HH:MM:SS,MIL
                startTime = match.group(1)
                if len(startTime) == 16:
                    startTime = startTime[:-4]
                elif len(startTime) == 8:
                    startTime += ",000"
                endTime = match.group(2)
                if len(endTime) == 16:
                    endTime = endTime[:-4]
                elif len(endTime) == 8:
                    endTime += ",000"
                output += "{start} --> {end}\r\n".format(start=startTime,end=endTime)
            else:
                # Fix text
                output += hp.unescape(line)
            
        f, path = mkstemp(suffix=".it.srt")
        os.write(f, output.encode('cp1252'))
        os.close(f)
        return path

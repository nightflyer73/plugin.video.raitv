# -*- coding: utf-8 -*-
import urllib2
import json

class RaiPlay:
    # From http://www.raiplay.it/mobile/prod/config/RaiPlay_Config.json
    baseUrl = "http://www.rai.it/"
    menuUrl = "http://www.rai.it/dl/RaiPlay/2016/menu/PublishingBlock-20b274b1-23ae-414f-b3bf-4bdc13b86af2.html?homejson"
    nothumb = "http://www.rai.it/cropgd/256x-/dl/components/img/imgPlaceholder.png"
    
    def getCountry(self):
        url = "http://mediapolisgs.rai.it/relinker/relinkerServlet.htm?cont=201342"
        response = urllib2.urlopen(url).read()
        return response
        
    def getMainMenu(self):
        response = json.load(urllib2.urlopen(self.menuUrl))
        # TODO: these entries must be filtered in default
        return response["menu"]

    # RaiPlay Genere Page
    # RaiPlay Tipologia Page
    def getCategory(self, url):
        response = json.load(urllib2.urlopen(url))
        return response["blocchi"]
  
    # Raiplay Tipologia Item
    def getProgrammeList(self, url):
        response = json.load(urllib2.urlopen(url))
        return response
    
    #  PLR programma Page
    def getProgramme(self, url):
        response = json.load(urllib2.urlopen(url))
        return response["Blocks"]
    
    def getContentSet(self, url):
        response = json.load(urllib2.urlopen(url))
        return response["items"]
    
    def getVideoUrl(self, pathId):
        response = json.load(urllib2.urlopen(self.baseUrl + pathId))
        url = response["video"]["contentUrl"]
        return url

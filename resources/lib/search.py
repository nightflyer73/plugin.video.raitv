# -*- coding: utf-8 -*-
import sys
import json
import urllib
import urllib2
import httplib
from xml.dom import minidom

class Search:
    _baseurl = "http://www.rai.tv"
    _nothumb = "http://www.rai.tv/dl/RaiTV/2012/images/NoAnteprimaItem.png"
    
    newsArchives = {"TG1": "Category:Edizioni integrali:Category-a18c6b01-37cf-4227-940c-e6b9b5dc592b",
        "TG2": "Category:Edizione integrale:Category-c765744f-e8a0-421c-99b8-35c93555db33",
        "TG3": "Category:Edizioni del TG3:Category-d404d0c9-fa2c-480f-9f1a-897414487f98"}
    
    newsProviders = {"TG1": "Tematica:TG1",
        "TG2": "Tematica:TG2",
        "TG3": "Tematica:TG3",
        "Rai News": "Tematica:Rai News",
        "Rai Sport": "Tematica:spt",
        "Rai Parlamento": "PageOB:Page-f3f817b3-1d55-4e99-8c36-464cea859189"}

    tematiche = ["Attualità", "Bianco e Nero", "Cinema", "Comici", "Cronaca", "Cucina", "Cultura", "Cultura e Spettacoli", "Economia", "Fiction",
        "Hi tech", "Inchieste", "Incontra", "Interviste", "Istituzioni", "Junior", "Moda", "Musica", "News", "Politica", "Promo", "Reality",
        "Salute", "Satira", "Scienza", "Società", "Spettacolo", "Sport", "Storia", "Telefilm", "Tempo libero", "Viaggi"]

    def searchText(self, text):
        # numero massimo di record in risposta
        num = 36
        # ordina per rilevanza (default su sito web)
        sort="date:D:L:d1"
        # ordina per data (default su app android)
        #sort="date:D:S:d1"
        url = "http://www.ricerca.rai.it/search?site=raitv&output=xml_no_dtd&proxystylesheet=json&client=json&sort=%s&filter=0&getfields=*&partialfields=videourl&num=%s&q=%s" % (sort, num, urllib.quote_plus(text))
        print "Search URL: %s" % url
        response = json.load(urllib2.urlopen(url))
        return response["list"]
    
    def getLastContentByTag(self, tags="", numContents=16):
        tags = urllib.quote(tags)
        domain = "RaiTv"
                
        url = "http://www.rai.tv/StatisticheProxy/proxyPost.jsp?action=getLastContentByTag&numContents=%s&tags=%s&domain=%s" % \
              (str(numContents), tags, domain)
        xmldata = urllib2.urlopen(url).read().lstrip()
        dom = minidom.parseString(xmldata)
 
        return self.parseResponse(dom)
    
    
    def getMostVisited(self, tags, days=7, numContents=16):
        tags = urllib.quote(tags)
        domain = "RaiTv"
        
        url = "http://www.rai.tv/StatisticheProxy/proxyPost.jsp?action=mostVisited&days=%s&state=1&records=%s&tags=%s&domain=%s" % \
            (str(days), str(numContents), tags, domain)
        xmldata = urllib2.urlopen(url).read().lstrip()
        dom = minidom.parseString(xmldata)    

        return self.parseResponse(dom)

        
    def parseResponse(self, dom):
        items = []
        
        for node in dom.getElementsByTagName('content'):
            # We don't handle photos
            typeNode = node.getElementsByTagName('type')
            if typeNode.length >= 1 and typeNode[0].childNodes[0].data == "Foto":
                continue
        
            item = {}
            item["title"] = node.getElementsByTagName('titolo')[0].childNodes[0].data
            #  "datacreazione" is always present
            item["date"] = node.getElementsByTagName('datacreazione')[0].childNodes[0].data[:10].replace("/",".")
            item["itemId"] = node.getElementsByTagName('localid')[0].childNodes[0].data
            
            descNode = node.getElementsByTagName('descrizione')
            if descNode.length > 0: 
                item["plotoutline"] = descNode[0].childNodes[0].data
            else:
                item["plotoutline"] = ""
            
            thumbNode = node.getElementsByTagName('pathImmagine')
            if thumbNode.length > 0:
                item["thumb"] = thumbNode[0].childNodes[0].data
                if item["thumb"][:4] != "http":
                    item["thumb"] = self._baseurl + item["thumb"]
                # Always use bigger thumbnail available
                item["thumb"] = item["thumb"].replace("/105x79","/")
            else:
                item["thumb"] = self._nothumb

            # Check if Video URL is present
            urlNode =  node.getElementsByTagName('h264')
            if urlNode.length > 0:
                item["url"] = urlNode[0].childNodes[0].data
            else:
                item["url"] = ""

            item["tvshowtitle"] = ""
            for tag in node.getElementsByTagName('tag'):
                if tag.childNodes[0].data[:13] == "NomeProgramma":
                    item["tvshowtitle"] = tag.childNodes[0].data[14:]
                    break

            items.append(item)

        return items


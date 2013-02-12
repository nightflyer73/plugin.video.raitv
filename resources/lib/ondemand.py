# -*- coding: cp1252 -*-
import sys
import urllib
import urllib2
import re
import json
from xml.dom import minidom

class OnDemand:
    _baseUrl = "http://www.rai.tv"
    
    def getProgrammeList(self):
        url = "http://www.rai.tv/dl/RaiTV/programmi/ricerca/ContentSet-6445de64-d321-476c-a890-ae4ed32c729e-darivedere.html"
        response = json.load(urllib2.urlopen(url))
        return response

    def search(self, index):
        programmes = self.getProgrammeList()
        result = []
        for programme in programmes:
            if programme["index"] == index:
                programme["pageId"] = programme["linkDemand"][25:-5]
                result.append(programme)
        return result

    def getProgrammeSets(self, pageId):
        url = "http://www.rai.tv/dl/RaiTV/programmi/%s.xml" % pageId
        xmldata = urllib2.urlopen(url).read()
        dom = minidom.parseString(xmldata)
        programmeSets = []
        for node in dom.getElementsByTagName('set'):
            name = node.attributes["name"].value
            uniquename = node.attributes["uniquename"].value
            try:
                types = node.getElementsByTagName('Summary')[0].getElementsByTagName('TypeOccurrency')
            except IndexError:
                types = []

            for typeoccurrency in types:
                # handle more than one media type
                mediatype = typeoccurrency.attributes["type"].value
                occurrency = typeoccurrency.attributes["occurrency"].value

                programmeSet = {}                
                programmeSet["name"] = name
                programmeSet["count"] = occurrency
                programmeSet["uniquename"] =  uniquename
                    
                if mediatype == "RaiTv Media Video Item":
                    programmeSet["mediatype"] = "V"
                    programmeSets.append(programmeSet)                         
                elif mediatype == "RaiTv Media Audio Item":
                    programmeSet["mediatype"] = "A"
                    programmeSets.append(programmeSet)                         
                elif mediatype == "RaiTv Media Podcast Item":
                    programmeSet["mediatype"] = "P"
                    programmeSets.append(programmeSet)                         
                elif mediatype == "RaiTv Media Foto Item":
                    pass
                    #programmeSet["mediatype"] = "F"
                    #programmeSets.append(programmeSet)

        return programmeSets

    def getItems(self, uniquename, count, mediatype):
        items = []
        i=0

        while len(items) < int(count):
            url = "http://www.rai.tv/dl/RaiTV/programmi/liste/%s-%s-%s.xml" % (uniquename, mediatype, i)
            xmldata = urllib2.urlopen(url).read()
            dom = minidom.parseString(xmldata)
            i = i + 1
            
            for node in dom.getElementsByTagName('item'):
                item = {}
                item["name"] = node.attributes['name'].value
                units = node.getElementsByTagName('units')[0]
                item["image"] = self._baseUrl + units.getElementsByTagName('imageUnit')[0].getElementsByTagName('image')[0].childNodes[0].data
                try:
                    item["date"] = units.getElementsByTagName('dateUnit')[0].getElementsByTagName('date')[0].childNodes[0].data
                except IndexError:
                    item["date"] = node.attributes['createDate'].value
                
                if mediatype == "V":
                    item["url"] = units.getElementsByTagName('videoUnit')[0].getElementsByTagName('url')[0].childNodes[0].data
                    # if present then get h264 url
                    attributes = units.getElementsByTagName('videoUnit')[0].getElementsByTagName('attribute')
                    for attribute in attributes:
                        if attribute.getElementsByTagName('key')[0].childNodes[0].data == "h264":
                            item["url"] = attribute.getElementsByTagName('value')[0].childNodes[0].data
                elif mediatype == "A":
                    item["url"] = self._baseUrl + units.getElementsByTagName('audioUnit')[0].getElementsByTagName('url')[0].childNodes[0].data
                elif mediatype == "F":
                    # do not handle photos
                    pass
                elif mediatype == "P":
                    item["url"] = units.getElementsByTagName('linkUnit')[0].getElementsByTagName('link')[0].childNodes[0].data
                    
                items.append(item)

        return items


#ondemand = OnDemand()
#print ondemand.search("b")
#print ondemand.getProgrammeSets("Page-5b3110f7-b13e-42e5-888d-c35e2119bf34")
#print ondemand.getItems("ContentSet-d77e7cf9-8688-4826-a9f3-736c9d1790b4", "29", "V")
#print ondemand.getItems("http://www.rai.tv/dl/RaiTV/programmi/liste/ContentSet-0c3cf090-9562-4de6-b204-39aca4848253-A-0.xml")
#print ondemand.getProgrammeSets("Page-f48c8dc0-351b-4765-96fa-38904b4ba863")
#print ondemand.getItems("http://www.rai.tv/dl/RaiTV/programmi/liste/ContentSet-4fe35ccb-6b29-4284-bad5-f9fa7a343b08-F-0.xml")
#print ondemand.getProgrammeSets("Page-a5ca5744-4390-41e9-925b-e9112705c830")
#print ondemand.getItems("http://www.rai.tv/dl/RaiTV/programmi/liste/ContentSet-c33f420f-62dc-4ed7-ba26-9684a1f97927-P-0.xml")
#print ondemand.getItems("http://www.rai.tv/dl/RaiTV/programmi/liste/ContentSet-13474b95-8e91-44e7-b1e0-9cb41387f1e9-V-0.xml")
#print ondemand.getProgrammeSets("Page-730a4f29-39e3-4796-83dd-236624e79c3f")
#print ondemand.getItems("http://www.rai.tv/dl/RaiTV/programmi/liste/ContentSet-4565a706-a94d-4387-9083-41a7e458c55c-V-0.xml")

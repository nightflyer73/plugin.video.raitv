import urllib2
import json

def get_tv_stations():
    url = "http://www.rai.it/dl/RaiPlay/2016/PublishingBlock-9a2ff311-fcf0-4539-8f8f-c4fee2a71d58.html?json"
    response = json.load(urllib2.urlopen(url))
    channels = response["dirette"]
    return channels
    
def get_radio_station():
    url = "http://rai.it/dl/portaleRadio/popup/ContentSet-003728e4-db46-4df8-83ff-606426c0b3f5-json.html"
    response = json.load(urllib2.urlopen(url))
    return response["dati"]

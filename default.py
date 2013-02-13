# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import datetime
import locale
import platform
from resources.lib.tgr import TGR
from resources.lib.search import Search
from resources.lib.onair import onAir
from resources.lib.replay import Replay
from resources.lib.ondemand import OnDemand
import resources.lib.stations as stations
import resources.lib.utils as utils

# plugin constants
__plugin__ = "plugin.video.raitv"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)

# plugin handle
handle = int(sys.argv[1])

# set italian locale
if  platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, 'ita_ita')
else:
    locale.setlocale(locale.LC_ALL, 'it_IT')

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addDirectoryItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=True)

def addLinkItem(parameters, li, url=""):
    if url == "":
        url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu '''
    liStyle = xbmcgui.ListItem("Dirette TV")
    addDirectoryItem({"mode": "live_tv"}, liStyle)
    liStyle = xbmcgui.ListItem("Dirette Radio",
        thumbnailImage="http://upload.wikimedia.org/wikipedia/it/f/f2/Radiorai_logo_2010.png")
    addDirectoryItem({"mode": "live_radio"}, liStyle)
    liStyle = xbmcgui.ListItem("Rai Replay")
    addDirectoryItem({"mode": "replay"}, liStyle)
    liStyle = xbmcgui.ListItem("Programmi On Demand")
    addDirectoryItem({"mode": "ondemand"}, liStyle)
    liStyle = xbmcgui.ListItem("Archivio Telegiornali")
    addDirectoryItem({"mode": "tg"}, liStyle)
    liStyle = xbmcgui.ListItem("Videonotizie")
    addDirectoryItem({"mode": "news"}, liStyle)
    liStyle = xbmcgui.ListItem("Aree tematiche")
    addDirectoryItem({"mode": "themes"}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_tg_root():
    search = Search()
    for k, v in search.newsArchives.iteritems():
        liStyle = xbmcgui.ListItem(k)
        addDirectoryItem({"mode": "get_last_content_by_tag",
            "tags": search.newsArchives[k]}, liStyle)    
    liStyle = xbmcgui.ListItem("TGR",
        thumbnailImage="http://www.tgr.rai.it/dl/tgr/mhp/immagini/splash.png")
    addDirectoryItem({"mode": "tgr"}, liStyle)  
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def show_tgr_root():
    #xbmcplugin.setContent(handle=handle, content='tvshows')
    
    tgr = TGR()
    programmes = tgr.getProgrammes()
    for programme in programmes:
        liStyle = xbmcgui.ListItem(programme["title"],
            thumbnailImage=programme["image"])
        addDirectoryItem({"mode": "tgr",
            "behaviour": programme["behaviour"],
            "url": programme["url"]}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_tgr_list(mode, url):
    #xbmcplugin.setContent(handle=handle, content='episodes')
    
    tgr = TGR()
    itemList = tgr.getList(url)
    for item in itemList:
        behaviour = item["behaviour"]
        if behaviour != "video":
            liStyle = xbmcgui.ListItem(item["title"])
            addDirectoryItem({"mode": "tgr",
                "behaviour": behaviour,
                "url": item["url"], }, liStyle)
        else:
            liStyle = xbmcgui.ListItem(item["title"])
            addLinkItem({"mode": "video",
                "title": item["title"],        
                "url": item["url"]}, liStyle)            
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


def play_video(title, url, thumbailUrl=""):
    item=xbmcgui.ListItem(title, thumbnailImage=thumbailUrl)
    item.setInfo(type="Video", infoLabels={"Title": title})
    xbmc.Player().play(url, item)

def show_tv_channels():
    for station in stations.station_info:
        if station["type"] == "tv":
            liStyle = xbmcgui.ListItem(station["name"])
            addLinkItem({"mode": "live_tv"}, liStyle, url=station["stream"]+"|viaurl=www.rai.tv")
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_radio_stations():
    for station in stations.station_info:
        if station["type"] == "radio":
            liStyle = xbmcgui.ListItem(station["name"],
                thumbnailImage=station["logo"])
            addLinkItem({"mode": "live_radio",
                "station_id": station["id"]}, liStyle, url=station["stream"])
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def play_radio(stationId):
    pass

def show_replay_channels():
    replay = Replay()
    channels = utils.sortedDictKeys(replay.channels)
    for channelId in channels:
        liStyle = xbmcgui.ListItem(replay.channels[channelId])
        addDirectoryItem({"mode": "replay",
            "channel_id": channelId}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_replay_dates(channelId):
    epgEndDate = datetime.date.today() - datetime.timedelta(days=1)
    epgStartDate = datetime.date.today() - datetime.timedelta(days=7)
    for single_date in utils.daterange(epgStartDate, epgEndDate):
        liStyle = xbmcgui.ListItem(single_date.strftime("%A %d %B").capitalize())
        addDirectoryItem({"mode": "replay",
            "channel_id": channelId,
            "date": single_date.strftime("%Y_%m_%d")}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_replay_epg(channelId, date):
    replay = Replay()
    programmes = replay.getProgrammes(int(channelId), date)

    # sort timetable
    timetable = utils.sortedDictKeys(programmes)

    for entry in timetable:
        if programmes[entry]["h264"] == "":
            # program is not available
            title = entry + " " + programmes[entry]["t"]
        else:
            title = "[COLOR blue]" + entry + " " + programmes[entry]["t"] + "[/COLOR]"
        liStyle = xbmcgui.ListItem(title,
            thumbnailImage=programmes[entry]["image"])
        addLinkItem({"mode": "video",
            "title": programmes[entry]["t"].encode('utf8'),        
            "url": programmes[entry]["h264"],
            "thumbnail": programmes[entry]["image"]}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)            

def show_ondemand_root():
    liStyle = xbmcgui.ListItem("0-9")
    addDirectoryItem({"mode": "ondemand",
        "index": "0"}, liStyle)
    for i in range(26):
        liStyle = xbmcgui.ListItem(chr(ord('A')+i))
        addDirectoryItem({"mode": "ondemand",
            "index": chr(ord('a')+i)}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_ondemand_index(index):
    ondemand = OnDemand()
    programmes = ondemand.search(index)
    for programme in programmes:
        liStyle = xbmcgui.ListItem(programme["title"],
            thumbnailImage=programme["image"])
        addDirectoryItem({"mode": "ondemand",
            "page_id": programme["pageId"]}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_ondemand_programme(pageId):
    liStyle = xbmcgui.ListItem("Più recenti")
    addDirectoryItem({"mode": "get_last_content_by_tag",
        "tags": "PageOB:"+pageId}, liStyle)

    liStyle = xbmcgui.ListItem("Più visti")
    addDirectoryItem({"mode": "get_most_visited",
        "tags": "PageOB:"+pageId}, liStyle)

    ondemand = OnDemand()
    psets = ondemand.getProgrammeSets(pageId)
    for pset in psets:
        liStyle = xbmcgui.ListItem(pset["name"])
        addDirectoryItem({"mode": "ondemand",
            "uniquename": pset["uniquename"],
            "count": pset["count"],
            "mediatype": pset["mediatype"]
            }, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_ondemand_items(uniquename, count, mediatype):
    ondemand = OnDemand()
    items = ondemand.getItems(uniquename, count, mediatype)
    for item in items:
        liStyle = xbmcgui.ListItem(item["name"], thumbnailImage=item["image"])
        liStyle.setInfo(type="Video", 
            infoLabels={"title": item["name"],
                "date": item["date"]})        
        addLinkItem({"mode": "video",
            "title": item["name"].encode('utf8'),        
            "url": item["url"],
            "thumbnail": item["image"]}, liStyle)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)   
    
def show_news_providers():
    search = Search()
    for k, v in search.newsProviders.iteritems():
        liStyle = xbmcgui.ListItem(k)
        addDirectoryItem({"mode": "get_last_content_by_tag",
            "tags": search.newsProviders[k]}, liStyle)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def show_themes():
    search = Search()
    for position, tematica in enumerate(search.tematiche):
        liStyle = xbmcgui.ListItem(tematica)
        addDirectoryItem({"mode": "get_last_content_by_tag",
            "tags": "Tematica:"+search.tematiche[int(position)]}, liStyle)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def get_last_content_by_tag(tags):
    search = Search()
    for item in search.getLastContentByTag(tags):
        liStyle = xbmcgui.ListItem(item["title"], thumbnailImage=item["thumb"])
        liStyle.setInfo(type="Video", 
            infoLabels={"title": item["title"],
                "date": item["date"],            
                "plotoutline": item["plotoutline"],
                "tvshowtitle": item["tvshowtitle"]})
        addLinkItem({"mode": "video",
            "title": item["title"].encode('utf8'),        
            "url": item["url"],
            "thumbnail": item["thumb"]}, liStyle)
    #xbmc.executebuiltin("Container.SetViewMode(502)")
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def get_most_visited(tags):
    search = Search()
    for item in search.getMostVisited(tags):
        liStyle = xbmcgui.ListItem(item["title"], thumbnailImage=item["thumb"])
        liStyle.setInfo(type="Video", 
            infoLabels={"title": item["title"],
                "date": item["date"],            
                "plotoutline": item["plotoutline"],
                "tvshowtitle": item["tvshowtitle"]})
        addLinkItem({"mode": "video",
            "title": item["title"].encode('utf8'),        
            "url": item["url"],
            "thumbnail": item["image"]}, liStyle)
    #xbmc.executebuiltin("Container.SetViewMode(502)")
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


# parameter values
params = parameters_string_to_dict(sys.argv[2])
mode = str(params.get("mode", ""))
behaviour = str(params.get("behaviour", ""))
url = str(params.get("url", ""))
title = str(params.get("title", ""))
thumbnail = str(params.get("thumbnail", ""))
date = str(params.get("date", ""))
channelId = str(params.get("channel_id", ""))
index = str(params.get("index", ""))
pageId = str(params.get("page_id", ""))
uniquename = str(params.get("uniquename", ""))
count = str(params.get("count", ""))
mediatype = str(params.get("mediatype", ""))
tags = str(params.get("tags", ""))

if mode == "live_tv":
    show_tv_channels()
elif mode == "live_radio":
    show_radio_stations()
elif mode == "replay":
    if channelId == "":
        show_replay_channels()
    elif date == "":
        show_replay_dates(channelId)
    else:
        show_replay_epg(channelId, date)
elif mode == "ondemand":
    if index != "":
        show_ondemand_index(index)
    elif pageId != "":
        show_ondemand_programme(pageId)
    elif uniquename != "":
        show_ondemand_items(uniquename, count, mediatype)
    else:
        show_ondemand_root()
elif mode == "tg":
    show_tg_root()
elif mode == "tgr":
    if url != "":
        show_tgr_list(mode, url)        
    else:
        show_tgr_root()        
elif mode == "news":
    show_news_providers()
elif mode == "themes":
    show_themes()
elif mode == "get_last_content_by_tag":
     get_last_content_by_tag(tags)
elif mode == "get_most_visited":
     get_most_visited(tags)     
elif mode == "video":
    play_video(title, url, thumbnail)
else:
    show_root_menu()


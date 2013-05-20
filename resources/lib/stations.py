import urllib2
import json

# TODO: Get channels once and not at every addon call
url = "http://www.rai.tv/dl/RaiTV/iphone/android/smartphone/advertising_config.html"
response = json.load(urllib2.urlopen(url))
tv_stations = response["Channels"]

url = "http://www.rai.tv/dl/RadioRai/config_json.html"
response = json.load(urllib2.urlopen(url))
radio_stations = response["canali"]

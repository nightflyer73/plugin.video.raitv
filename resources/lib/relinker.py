import urllib2
import re

class Relinker:
    def getURL(self, url):
        request = urllib2.Request(url, headers={"viaurl" : "www.rai.tv"})
        response = urllib2.urlopen(request)
        headers = response.info()
        headers.dict

        if url != response.geturl():
            # A redirect occured
            mediaUrl = response.geturl()
        elif headers["Content-Type"].find("charset=ISO-8859-1") != -1:
            # Content-Type is misleading!!!
            body = response.read().strip()
            # Guess file type from body content
            if body[:7] == "http://":
                # Get the URL from the  body
                mediaUrl = body
            elif body[:4] == "<ASX":
                # Parse ASX file and get the first URL in the playlist
                # XML is often malformed!!!
                match=re.compile('<REF\s+HREF="(.+?)"').findall(body)
                mediaUrl = match[0]
            else:
                # Media type non supported
                # e.g. Microsoft Smooth Streaming
                mediaUrl = ""
        
        return mediaUrl

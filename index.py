import os
from urllib.parse import urlparse
from urllib.request import urlopen, urlretrieve

from bs4 import BeautifulSoup

downloadDir = "downloaded"
baseUrl = "https://pythonscraping.com/"
baseNetloc = urlparse(baseUrl).netloc


def getAbsoluteURL(source):
    if urlparse(baseUrl).netloc == "":
        return baseUrl + source
    return source


def getDownloadPath(fileUrl):
    parsed = urlparse(fileUrl)
    netloc = parsed.netloc.strip("/")
    path = parsed.path.strip("/")
    localfile = f"{downloadDir}/{netloc}/{path}"

    localpath = "/".join(localfile.split("/")[:-1])
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    return localfile


html = urlopen(baseUrl)
bs = BeautifulSoup(html, "html.parser")
downloadList = bs.find_all(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(download["src"])
    if fileUrl is not None:
        try:
            urlretrieve(fileUrl, getDownloadPath(fileUrl))
            print(fileUrl)
        except Exception as e:
            print(f"Could not retrieve {fileUrl} Error: {e}")

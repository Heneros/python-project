from urllib.request import urlopen

from bs4 import BeautifulSoup

# try:
#     html = urlopen("http://pythonscraping.com/pages/page1.html")
# except HTTPError as e:
#     print(e)
# except URLError:
#     print("The server could not be found!")
#     # bs = BeautifulSoup(html.read(), 'html.parser')
# else:
#     print("IT'S ALIVE")


# def getTitle(url):
#     try:
#         html = urlopen(url)
#     except HTTPError:
#         return None
#     try:
#         bs = BeautifulSoup(html.read(), "html.parser")
#         nameList = bs.find_all("span", {"class": "green"})
#         # title = bs.body.h1
#         for name in nameList:
#             print(name.get_text())

#     except AttributeError:
#         return None
#     return name.get_text()


# title = getTitle("http://www.pythonscraping.com/pages/page1.html")

# if title == None:
#     print("Title could not be found")
# else:
#     print(title)

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html, "html.parser")

for child in bs.find("table", {"id": "giftList"}).children:
    print(child)

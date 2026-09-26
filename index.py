import datetime
import random
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

random.seed(datetime.datetime.now().timestamp())


# pages = set()


# def getLinks(articleUrl):
#     req = Request(
#         f"http://en.wikipedia.org{articleUrl}",
#         headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         },
#     )
#     html = urlopen(req)
#     bs = BeautifulSoup(html, "html.parser")

#     try:
#         print(bs.h1.getText())
#         bodyContent = bs.find("div", {"id": "bodyContent"}).find_all("p")
#         if len(bodyContent):
#             print(bodyContent[0])
#         print(bs.find(id="ca-edit").find("a").attrs["href"])
#         print(bs.h1.get_text())
#         print(bs.find(id="mw-content-text").find_all("p")[0])
#         print(bs.find(id="ca-edit").find("span").find("a").attrs["href"])
#     except AttributeError:
#         print("This page is missing something! Continuing.")

#     for link in bs.find_all("a", href=re.compile("^(/wiki/)")):
#         if "href" in link.attrs:
#             if link.attrs["href"] not in pages:
#                 newPage = link.attrs["href"]
#                 print("-" * 20)
#                 print(newPage)
#                 pages.add(newPage)
#                 getLinks(newPage)


# getLinks("/wiki/Kevin_Bacon")


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f"TITLE: {self.title}")
        print(f"URL: {self.url}")
        print(f"BODY:\n {self.body}")


def scrapeCNN(url):
    bs = BeautifulSoup(urlopen(url))
    title = bs.find("h1").text
    body = bs.find("div", {"class": "article__content"}).text
    print("body: ")
    print(body)
    return Content(url, title, body)


def scrapeBrookings(url):
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    html = urlopen(req)
    bs = BeautifulSoup(html, "html.parser")
    title = bs.find("h1")
    body = bs.find("div", {"class": "post-body"})
    return Content(url, title, body)


url = "https://www.brookings.edu/research/robotic-rulemaking/"
content = scrapeBrookings(url)
content.print()

url = "https://www.cnn.com/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html"
content = scrapeCNN(url)
content.print()
